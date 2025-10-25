"""Tests for process management."""
import logging
import os
import signal
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import psutil
import pytest

from metaexpert.cli.core.exceptions import ProcessError
from metaexpert.cli.process.manager import ProcessInfo, ProcessManager


@pytest.fixture
def temp_pid_dir(tmp_path: Path) -> Path:
    """Create a temporary PID directory."""
    pid_dir = tmp_path / "pids"
    pid_dir.mkdir()
    return pid_dir


@pytest.fixture
def process_manager(temp_pid_dir: Path) -> ProcessManager:
    """Create a ProcessManager instance."""
    return ProcessManager(pid_dir=temp_pid_dir)


@pytest.fixture
def sample_project(tmp_path: Path) -> Path:
    """Create a sample project directory."""
    project = tmp_path / "test-project"
    project.mkdir()
    (project / "main.py").write_text("# Sample script\nprint('Hello')")
    return project


def test_process_manager_initialization(temp_pid_dir: Path) -> None:
    """Test ProcessManager initialization."""
    manager = ProcessManager(pid_dir=temp_pid_dir)
    assert manager.pid_dir == temp_pid_dir
    assert temp_pid_dir.exists()


def test_get_pid_file(process_manager: ProcessManager, sample_project: Path) -> None:
    """Test getting PID file path."""
    pid_file = process_manager._get_pid_file(sample_project)
    expected = process_manager.pid_dir / f"{sample_project.name}.pid"
    assert pid_file == expected


def test_read_pid_valid(process_manager: ProcessManager, sample_project: Path) -> None:
    """Test reading valid PID from file."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid_file.write_text("12345")
    
    pid = process_manager._read_pid(pid_file)
    assert pid == 12345


def test_read_pid_invalid(process_manager: ProcessManager, sample_project: Path) -> None:
    """Test reading invalid PID from file."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid_file.write_text("invalid")
    
    pid = process_manager._read_pid(pid_file)
    assert pid is None


def test_read_pid_nonexistent(process_manager: ProcessManager, sample_project: Path) -> None:
    """Test reading PID from nonexistent file."""
    pid_file = process_manager._get_pid_file(sample_project)
    # Ensure file doesn't exist
    assert not pid_file.exists()
    
    pid = process_manager._read_pid(pid_file)
    assert pid is None


def test_is_running_no_pid_file(process_manager: ProcessManager, sample_project: Path) -> None:
    """Test is_running when PID file doesn't exist."""
    assert not process_manager.is_running(sample_project)


def test_is_running_pid_file_empty(process_manager: ProcessManager, sample_project: Path) -> None:
    """Test is_running when PID file is empty."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid_file.write_text("")
    
    assert not process_manager.is_running(sample_project)


def test_is_running_process_does_not_exist(
    process_manager: ProcessManager, 
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test is_running when process doesn't exist."""
    # Mock psutil.Process to raise NoSuchProcess
    mock_process = MagicMock()
    mock_process.is_running.return_value = False
    mock_process.status.return_value = psutil.STATUS_RUNNING
    
    with patch("psutil.Process", return_value=mock_process):
        pid_file = process_manager._get_pid_file(sample_project)
        pid_file.write_text("999999")  # Non-existent PID
        
        assert not process_manager.is_running(sample_project)


def test_is_running_process_zombie(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test is_running when process is a zombie."""
    # Mock psutil.Process to return STATUS_ZOMBIE
    mock_process = MagicMock()
    mock_process.is_running.return_value = True
    mock_process.status.return_value = psutil.STATUS_ZOMBIE
    
    with patch("psutil.Process", return_value=mock_process):
        pid_file = process_manager._get_pid_file(sample_project)
        pid_file.write_text("12345")
        
        assert not process_manager.is_running(sample_project)


def test_is_running_process_running(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test is_running when process is actually running."""
    # Mock psutil.Process to return a running process
    mock_process = MagicMock()
    mock_process.is_running.return_value = True
    mock_process.status.return_value = psutil.STATUS_RUNNING
    
    with patch("psutil.Process", return_value=mock_process):
        pid_file = process_manager._get_pid_file(sample_project)
        pid_file.write_text("12345")
        
        assert process_manager.is_running(sample_project)


def test_start_already_running(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test starting a process that's already running."""
    # Mock is_running to return True
    with patch.object(process_manager, "is_running", return_value=True):
        with pytest.raises(ProcessError, match="already running"):
            process_manager.start(sample_project)


def test_start_script_not_found(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test starting when script doesn't exist."""
    nonexistent_script = "nonexistent.py"
    
    with pytest.raises(ProcessError, match="Script not found"):
        process_manager.start(sample_project, script=nonexistent_script)


def test_start_attached_success(
    process_manager: ProcessManager,
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test successful attached process start."""
    # Mock subprocess.Popen to return a mock process
    mock_process = MagicMock()
    mock_process.pid = 54321
    
    # Mock PIDFileLock context manager
    with patch("metaexpert.cli.process.manager.PIDFileLock") as mock_pid_lock:
        with patch("subprocess.Popen", return_value=mock_process):
            with patch.object(process_manager, "is_running", side_effect=[False, True]):
                pid = process_manager.start(sample_project, detach=False)
                
                assert pid == 54321
                # Check that PID file was written
                pid_file = process_manager._get_pid_file(sample_project)
                assert pid_file.exists()
                assert pid_file.read_text().strip() == "54321"


def test_start_detached_success(
    process_manager: ProcessManager,
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test successful detached process start."""
    # Mock subprocess.Popen to return a mock process
    mock_process = MagicMock()
    mock_process.pid = 54322
    
    # Mock PIDFileLock context manager
    with patch("metaexpert.cli.process.manager.PIDFileLock") as mock_pid_lock:
        with patch("subprocess.Popen", return_value=mock_process):
            with patch.object(process_manager, "is_running", side_effect=[False, True]):
                pid = process_manager.start(sample_project, detach=True)
                
                assert pid == 54322
                # Check that PID file was written
                pid_file = process_manager._get_pid_file(sample_project)
                assert pid_file.exists()
                assert pid_file.read_text().strip() == "54322"


def test_start_failure(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test process start failure."""
    with patch("subprocess.Popen", side_effect=OSError("Permission denied")):
        with patch.object(process_manager, "is_running", return_value=False):
            with pytest.raises(ProcessError, match="Failed to start process"):
                process_manager.start(sample_project)


def test_stop_not_running(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test stopping a process that's not running."""
    with patch.object(process_manager, "is_running", return_value=False):
        with pytest.raises(ProcessError, match="No running expert found"):
            process_manager.stop(sample_project)


def test_stop_graceful_success(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test successful graceful process stop."""
    # Mock psutil.Process
    mock_process = MagicMock()
    mock_process.wait.return_value = None  # Process terminates successfully
    
    with patch("psutil.Process", return_value=mock_process):
        with patch.object(process_manager, "is_running", side_effect=[True, False]):
            # Create a PID file
            pid_file = process_manager._get_pid_file(sample_project)
            pid_file.write_text("12345")
            
            process_manager.stop(sample_project, timeout=1)
            
            # Check that terminate was called
            mock_process.terminate.assert_called_once()
            # Check that PID file was removed
            assert not pid_file.exists()


def test_stop_force_kill(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test force killing a process."""
    # Mock psutil.Process
    mock_process = MagicMock()
    
    with patch("psutil.Process", return_value=mock_process):
        with patch.object(process_manager, "is_running", return_value=True):
            # Create a PID file
            pid_file = process_manager._get_pid_file(sample_project)
            pid_file.write_text("12345")
            
            process_manager.stop(sample_project, force=True)
            
            # Check that kill was called
            mock_process.kill.assert_called_once()
            # Check that PID file was removed
            assert not pid_file.exists()


def test_stop_timeout_then_force(
    process_manager: ProcessManager,
    sample_project: Path
) -> None:
    """Test timeout during graceful stop, then force kill."""
    # Mock psutil.Process
    mock_process = MagicMock()
    # First call to wait() will timeout, second call will succeed
    mock_process.wait.side_effect = [psutil.TimeoutExpired(1), None] # First timeout, then success when force=True
    
    with patch("psutil.Process", return_value=mock_process):
        with patch.object(process_manager, "is_running", side_effect=[True, True]):  # Process is running both times
            # Create a PID file
            pid_file = process_manager._get_pid_file(sample_project)
            pid_file.write_text("12345")
            
            # First call with force=False should raise ProcessError due to timeout
            with pytest.raises(ProcessError, match="did not terminate within"):
                process_manager.stop(sample_project, timeout=1, force=False)
            
            # Now call with force=True, which should call kill directly
            process_manager.stop(sample_project, force=True)
            
            # Check that terminate was called once (from first call) and kill was called once (from second call)
            mock_process.terminate.assert_called_once()
            mock_process.kill.assert_called_once()
            # Check that PID file was removed
            assert not pid_file.exists()


def test_stop_timeout_no_force(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test timeout during graceful stop without force."""
    # Mock psutil.Process
    mock_process = MagicMock()
    mock_process.wait.side_effect = psutil.TimeoutExpired(1)  # Timeout on wait
    
    with patch("psutil.Process", return_value=mock_process):
        with patch.object(process_manager, "is_running", return_value=True):
            # Create a PID file
            pid_file = process_manager._get_pid_file(sample_project)
            pid_file.write_text("12345")
            
            with pytest.raises(ProcessError, match="did not terminate within"):
                process_manager.stop(sample_project, timeout=1, force=False)
            
            # Check that terminate was called
            mock_process.terminate.assert_called_once()
            # Check that kill was NOT called
            mock_process.kill.assert_not_called()
            # Check that PID file still exists
            assert pid_file.exists()


def test_stop_process_already_dead(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test stopping a process that's already dead."""
    # Mock psutil.Process to raise NoSuchProcess
    with patch("psutil.Process", side_effect=psutil.NoSuchProcess(12345)):
        with patch.object(process_manager, "is_running", return_value=True):
            # Create a PID file
            pid_file = process_manager._get_pid_file(sample_project)
            pid_file.write_text("12345")
            
            # Should not raise an exception, and should clean up PID file
            process_manager.stop(sample_project)
            
            # Check that PID file was removed
            assert not pid_file.exists()


def test_get_info_not_running(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test get_info when process is not running."""
    with patch.object(process_manager, "is_running", return_value=False):
        info = process_manager.get_info(sample_project)
        assert info is None


def test_get_info_success(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test successful get_info."""
    # Mock psutil.Process
    mock_process = MagicMock()
    mock_process.create_time.return_value = datetime.now().timestamp()
    mock_process.status.return_value = psutil.STATUS_RUNNING
    mock_process.memory_info.return_value.rss = 1024 * 1024  # 1MB
    mock_process.cpu_percent.return_value = 5.5
    
    with patch("psutil.Process", return_value=mock_process):
        with patch.object(process_manager, "is_running", return_value=True):
            # Create a PID file
            pid_file = process_manager._get_pid_file(sample_project)
            pid_file.write_text("12345")
            
            info = process_manager.get_info(sample_project)
            
            assert isinstance(info, ProcessInfo)
            assert info.pid == 12345
            assert info.name == sample_project.name
            assert info.project_path == sample_project
            assert info.status == psutil.STATUS_RUNNING
            assert info.memory_mb == 1.0
            assert info.cpu_percent == 5.5


def test_get_info_process_gone(
    process_manager: ProcessManager, 
    sample_project: Path
) -> None:
    """Test get_info when process disappears during info retrieval."""
    # Mock psutil.Process to raise NoSuchProcess
    with patch("psutil.Process", side_effect=psutil.NoSuchProcess(12345)):
        with patch.object(process_manager, "is_running", return_value=True):
            # Create a PID file
            pid_file = process_manager._get_pid_file(sample_project)
            pid_file.write_text("12345")
            
            info = process_manager.get_info(sample_project)
            assert info is None


def test_list_running_no_processes(process_manager: ProcessManager, tmp_path: Path) -> None:
    """Test list_running when no processes are running."""
    # Create a dummy project directory
    project_dir = tmp_path / "projects"
    project_dir.mkdir()
    
    with patch.object(process_manager, "is_running", return_value=False):
        running = process_manager.list_running(search_path=project_dir)
        assert running == []


def test_list_running_with_processes(
    process_manager: ProcessManager,
    tmp_path: Path
) -> None:
    """Test list_running with some processes."""
    # Create a dummy project directory
    project_dir = tmp_path / "projects"
    project_dir.mkdir()
    
    test_project = project_dir / "test-project"
    test_project.mkdir()
    
    # Create a mock ProcessInfo
    mock_info = ProcessInfo(
        pid=12345,
        name="test-project",
        project_path=test_project,
        started_at=datetime.now(),
        status="running",
        memory_mb=10.5,
        cpu_percent=2.3
    )
    
    with patch.object(process_manager, "is_running", return_value=True):
        with patch.object(process_manager, "get_info", return_value=mock_info):
            # Create a PID file to simulate a running process
            pid_file = process_manager.pid_dir / "test-project.pid"
            pid_file.write_text("12345")
            
            running = process_manager.list_running(search_path=project_dir)
            
            assert len(running) == 1
            assert running[0] == mock_info


def test_process_info_dataclass() -> None:
    """Test ProcessInfo dataclass."""
    now = datetime.now()
    info = ProcessInfo(
        pid=12345,
        name="test",
        project_path=Path("/tmp/test"),
        started_at=now,
        status="running",
        memory_mb=10.5,
        cpu_percent=2.3
    )
    
    assert info.pid == 12345
    assert info.name == "test"
    assert info.project_path == Path("/tmp/test")
    assert info.started_at == now
    assert info.status == "running"
    assert info.memory_mb == 10.5
    assert info.cpu_percent == 2.3


def test_write_pid_file_success(process_manager: ProcessManager, sample_project: Path) -> None:
    """Test writing PID to file using PIDFileLock."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid = 12345
    
    # This tests that the PID file is properly written during start
    with patch("metaexpert.cli.process.manager.PIDFileLock"):
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.pid = pid
            mock_popen.return_value = mock_process
            
            with patch.object(process_manager, "is_running", side_effect=[False, True]):
                # Call start which internally writes the PID
                result_pid = process_manager.start(sample_project, detach=False)
                
                assert result_pid == pid
                assert pid_file.exists()
                assert pid_file.read_text().strip() == str(pid)


def test_delete_pid_file_on_stop(process_manager: ProcessManager, sample_project: Path) -> None:
    """Test that PID file is deleted when stopping a process."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid_file.write_text("12345")
    
    # Mock the process for stopping
    mock_process = MagicMock()
    
    with patch("psutil.Process", return_value=mock_process):
        with patch.object(process_manager, "is_running", side_effect=[True, False]):
            process_manager.stop(sample_project)
            
            # Check that PID file was removed
            assert not pid_file.exists()


def test_start_process_error_handling_with_logging(
    process_manager: ProcessManager,
    sample_project: Path,
    caplog: pytest.LogCaptureFixture
) -> None:
    """Test logging during process start errors."""
    with patch("subprocess.Popen", side_effect=OSError("Permission denied")):
        with patch.object(process_manager, "is_running", return_value=False):
            with pytest.raises(ProcessError, match="Failed to start process"):
                with caplog.at_level(logging.ERROR):
                    process_manager.start(sample_project)
                    
                    # Check that error was logged
                    assert "Failed to start process" in caplog.text


def test_stop_process_error_handling_with_logging(
    process_manager: ProcessManager,
    sample_project: Path,
    caplog: pytest.LogCaptureFixture
) -> None:
    """Test logging during process stop errors."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid_file.write_text("12345")
    
    # Mock a process that causes an error during stop
    mock_process = MagicMock()
    mock_process.kill.side_effect = psutil.AccessDenied()
    
    with patch("psutil.Process", return_value=mock_process):
        with patch.object(process_manager, "is_running", return_value=True):
            with pytest.raises(ProcessError, match="Failed to stop process"):
                with caplog.at_level(logging.ERROR):
                    process_manager.stop(sample_project, force=True)
                    
                    # Check that error was logged
                    assert "Failed to stop process" in caplog.text


def test_list_running_filter_by_project_path(
    process_manager: ProcessManager,
    tmp_path: Path
) -> None:
    """Test list_running with specific project path filtering."""
    # Create two project directories
    project_dir = tmp_path / "projects"
    project_dir.mkdir()
    
    project1 = project_dir / "project1"
    project1.mkdir()
    
    project2 = project_dir / "project2"
    project2.mkdir()
    
    # Create PID files for both projects
    pid_file1 = process_manager.pid_dir / "project1.pid"
    pid_file1.write_text("11111")
    
    pid_file2 = process_manager.pid_dir / "project2.pid"
    pid_file2.write_text("22222")
    
    # Mock running processes for both projects
    mock_info1 = ProcessInfo(
        pid=1111,
        name="project1",
        project_path=project1,
        started_at=datetime.now(),
        status="running",
        memory_mb=10.5,
        cpu_percent=2.3
    )
    
    mock_info2 = ProcessInfo(
        pid=22222,
        name="project2",
        project_path=project2,
        started_at=datetime.now(),
        status="running",
        memory_mb=15.2,
        cpu_percent=3.1
    )
    
    # Mock is_running to return True for both projects
    def mock_is_running(project_path):
        return project_path in [project1, project2]
    
    # Mock get_info to return appropriate info based on project
    def mock_get_info(project_path):
        if project_path == project1:
            return mock_info1
        elif project_path == project2:
            return mock_info2
        return None
    
    with patch.object(process_manager, "is_running", side_effect=mock_is_running):
        with patch.object(process_manager, "get_info", side_effect=mock_get_info):
            # List all running processes
            all_running = process_manager.list_running(search_path=project_dir)
            assert len(all_running) == 2
            
            # The search_path parameter actually filters by looking for project directories
            # under the search_path, so this test verifies that functionality


def test_list_running_no_matching_processes(
    process_manager: ProcessManager,
    tmp_path: Path
) -> None:
    """Test list_running when no processes match the search path."""
    # Create a search directory without any corresponding PID files
    search_dir = tmp_path / "search_dir"
    search_dir.mkdir()
    
    # Create a PID file for a project that doesn't exist in search path
    pid_file = process_manager.pid_dir / "nonexistent_project.pid"
    pid_file.write_text("12345")
    
    with patch.object(process_manager, "is_running", return_value=False):
        running = process_manager.list_running(search_path=search_dir)
        assert running == []


def test_start_detached_windows_specific(
    process_manager: ProcessManager,
    sample_project: Path
) -> None:
    """Test detached start with Windows-specific parameters."""
    mock_process = MagicMock()
    mock_process.pid = 54323
    
    with patch("metaexpert.cli.process.manager.PIDFileLock"):
        with patch("sys.platform", "win32"):
            with patch("subprocess.Popen", return_value=mock_process) as mock_popen:
                with patch.object(process_manager, "is_running", side_effect=[False, True]):
                    pid = process_manager.start(sample_project, detach=True)
                    
                    assert pid == 54323
                    # Check that Windows-specific creationflags were used
                    mock_popen.assert_called_once()
                    args, kwargs = mock_popen.call_args
                    assert "creationflags" in kwargs
                    # DETACHED_PROCESS (8) | CREATE_NEW_PROCESS_GROUP (512) = 520
                    assert kwargs["creationflags"] == (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)


def test_start_detached_unix_specific(
    process_manager: ProcessManager,
    sample_project: Path
) -> None:
    """Test detached start with Unix-specific parameters."""
    mock_process = MagicMock()
    mock_process.pid = 54324
    
    with patch("metaexpert.cli.process.manager.PIDFileLock"):
        with patch("sys.platform", "linux"):
            with patch("subprocess.Popen", return_value=mock_process) as mock_popen:
                with patch.object(process_manager, "is_running", side_effect=[False, True]):
                    pid = process_manager.start(sample_project, detach=True)
                    
                    assert pid == 54324
                    # Check that Unix-specific start_new_session was used
                    mock_popen.assert_called_once()
                    args, kwargs = mock_popen.call_args
                    assert "start_new_session" in kwargs
                    assert kwargs["start_new_session"] is True


def test_stop_process_access_denied(
    process_manager: ProcessManager,
    sample_project: Path
) -> None:
    """Test stopping a process when access is denied."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid_file.write_text("12345")
    
    # Mock psutil.Process to raise AccessDenied
    with patch("psutil.Process", side_effect=psutil.AccessDenied(12345)):
        with patch.object(process_manager, "is_running", return_value=True):
            with pytest.raises(ProcessError, match="Failed to stop process"):
                process_manager.stop(sample_project)


def test_get_info_process_access_denied(
    process_manager: ProcessManager,
    sample_project: Path
) -> None:
    """Test get_info when access to process is denied."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid_file.write_text("12345")
    
    # Mock psutil.Process to raise AccessDenied
    with patch("psutil.Process", side_effect=psutil.AccessDenied(12345)):
        with patch.object(process_manager, "is_running", return_value=True):
            info = process_manager.get_info(sample_project)
            assert info is None


def test_is_running_access_denied(
    process_manager: ProcessManager,
    sample_project: Path
) -> None:
    """Test is_running when access to process is denied."""
    pid_file = process_manager._get_pid_file(sample_project)
    pid_file.write_text("12345")
    
    # Mock psutil.Process to raise AccessDenied
    with patch("psutil.Process", side_effect=psutil.AccessDenied(12345)):
        result = process_manager.is_running(sample_project)
        assert result is False