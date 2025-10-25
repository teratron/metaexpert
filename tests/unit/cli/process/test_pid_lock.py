"""Tests for PID file locking."""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from metaexpert.cli.process.pid_lock import PIDFileLock, check_pid_file_status, is_pid_running


@pytest.fixture
def temp_pid_file(tmp_path: Path) -> Path:
    """Create a temporary PID file path."""
    return tmp_path / "test.pid"


def test_pid_file_lock_initialization(temp_pid_file: Path) -> None:
    """Test PIDFileLock initialization."""
    lock = PIDFileLock(temp_pid_file)
    assert lock.pid_file == temp_pid_file
    assert lock.fd is None
    assert lock._locked is False


def test_pid_file_lock_enter_creates_parent_dirs(temp_pid_file: Path) -> None:
    """Test that entering the context creates parent directories."""
    nested_pid_file = temp_pid_file.parent / "subdir" / "test.pid"
    assert not nested_pid_file.parent.exists()
    
    with PIDFileLock(nested_pid_file):
        assert nested_pid_file.parent.exists()
        assert nested_pid_file.parent.is_dir()


def test_pid_file_lock_enter_unix_success(temp_pid_file: Path) -> None:
    """Test successful lock acquisition on Unix-like systems."""
    if sys.platform == "win32":
        pytest.skip("Unix-specific test")
    
    with patch("fcntl.flock") as mock_flock:
        with PIDFileLock(temp_pid_file) as lock:
            assert lock._locked is True
            assert lock.fd is not None
            # Check that flock was called with LOCK_EX | LOCK_NB
            mock_flock.assert_called_once()
            args, kwargs = mock_flock.call_args
            fd_arg, flags_arg = args
            assert fd_arg == lock.fd
            # fcntl.LOCK_EX | fcntl.LOCK_NB = 2 | 4 = 6
            assert flags_arg == 6


def test_pid_file_lock_enter_windows_success(temp_pid_file: Path) -> None:
    """Test successful lock acquisition on Windows."""
    if sys.platform != "win32":
        pytest.skip("Windows-specific test")
    
    # Import msvcrt to get the actual constant values
    import msvcrt
    lk_nblck = getattr(msvcrt, 'LK_NBLCK', 1)  # Default to 1 if not available during testing
    
    with patch("msvcrt.locking") as mock_locking:
        with PIDFileLock(temp_pid_file) as lock:
            assert lock._locked is True
            assert lock.fd is not None
            # Check that msvcrt.locking was called
            mock_locking.assert_called_once()
            args, kwargs = mock_locking.call_args
            fd_arg, mode_arg, nbytes_arg = args
            assert fd_arg == lock.fd
            # The mode should match the LK_NBLCK constant
            assert mode_arg == lk_nblck
            assert nbytes_arg == 1  # This is the number of bytes to lock


def test_pid_file_lock_enter_blocked_unix(temp_pid_file: Path) -> None:
    """Test lock acquisition failure due to blocking on Unix."""
    if sys.platform == "win32":
        pytest.skip("Unix-specific test")
    
    with patch("fcntl.flock", side_effect=BlockingIOError()):
        with pytest.raises(RuntimeError, match="already locked"):
            with PIDFileLock(temp_pid_file):
                pass  # Should not reach here


def test_pid_file_lock_enter_blocked_windows(temp_pid_file: Path) -> None:
    """Test lock acquisition failure due to blocking on Windows."""
    if sys.platform != "win32":
        pytest.skip("Windows-specific test")
    
    with patch("msvcrt.locking", side_effect=BlockingIOError()):
        with pytest.raises(RuntimeError, match="already locked"):
            with PIDFileLock(temp_pid_file):
                pass  # Should not reach here


def test_pid_file_lock_exit_unlocks_unix(temp_pid_file: Path) -> None:
    """Test that exiting the context unlocks the file on Unix."""
    if sys.platform == "win32":
        pytest.skip("Unix-specific test")
    
    with patch("fcntl.flock") as mock_flock:
        with PIDFileLock(temp_pid_file) as lock:
            fd = lock.fd
            assert lock._locked is True
        
        # Check that flock was called twice: once for lock, once for unlock
        assert mock_flock.call_count == 2
        # The second call should be unlock (fcntl.LOCK_UN = 8)
        args, kwargs = mock_flock.call_args_list[1]
        fd_arg, flags_arg = args
        assert fd_arg == fd
        assert flags_arg == 8  # fcntl.LOCK_UN


def test_pid_file_lock_exit_unlocks_windows(temp_pid_file: Path) -> None:
    """Test that exiting the context unlocks the file on Windows."""
    if sys.platform != "win32":
        pytest.skip("Windows-specific test")
    
    # Import msvcrt to get the actual constant values
    import msvcrt
    lk_unlck = getattr(msvcrt, 'LK_UNLCK', 2)  # Default to 2 if not available during testing
    
    with patch("msvcrt.locking") as mock_locking:
        with PIDFileLock(temp_pid_file) as lock:
            fd = lock.fd
            assert lock._locked is True
    
        # Check that msvcrt.locking was called twice: once for lock, once for unlock
        assert mock_locking.call_count == 2
        # The second call should be unlock (msvcrt.LK_UNLCK)
        args, kwargs = mock_locking.call_args_list[1]
        fd_arg, mode_arg, nbytes_arg = args
        assert fd_arg == fd
        assert mode_arg == lk_unlck  # msvcrt.LK_UNLCK
        assert nbytes_arg == 1


def test_pid_file_lock_exit_closes_fd(temp_pid_file: Path) -> None:
    """Test that exiting the context closes the file descriptor."""
    original_close = os.close
    
    with patch("os.close") as mock_close:
        with PIDFileLock(temp_pid_file) as lock:
            fd = lock.fd
            assert fd is not None
        
        # Check that os.close was called with the file descriptor
        mock_close.assert_called_once_with(fd)
        assert lock.fd is None


def test_pid_file_lock_exit_handles_exception_in_unlock(
    temp_pid_file: Path
) -> None:
    """Test that exit handles exceptions during unlock gracefully."""
    if sys.platform == "win32":
        pytest.skip("Unix-specific test for this example")
    
    with patch("fcntl.flock", side_effect=[None, OSError("Unlock failed")]):
        with patch("os.close") as mock_close:
            with PIDFileLock(temp_pid_file) as lock:
                fd = lock.fd
                assert lock._locked is True
            
            # Even if unlock fails, os.close should still be called
            mock_close.assert_called_once_with(fd)
            assert lock.fd is None


def test_pid_file_lock_multiple_locks_same_file(temp_pid_file: Path) -> None:
    """Test that multiple locks on the same file fail as expected."""
    if sys.platform == "win32":
        # On Windows, test with mocked file locking
        # Need to provide side_effect for both locking and unlocking calls
        # The sequence is: first lock (success), second lock (fail with BlockingIOError)
        # When second lock fails, it doesn't reach the __exit__ method,
        # but first context manager will still try to unlock
        with patch("msvcrt.locking") as mock_locking:
            # First context: lock succeeds, then unlock happens when exiting
            # Second context: lock fails with BlockingIOError (no unlock call since __enter__ fails)
            # Total sequence: lock1, lock2(fail), unlock1
            mock_locking.side_effect = [None, BlockingIOError(), None]  # First lock, second lock (should fail), first unlock
            with patch("os.open", return_value=123):
                with patch("os.close"):
                    # Acquire first lock
                    with PIDFileLock(temp_pid_file):
                        # Try to acquire second lock - should fail
                        with pytest.raises(RuntimeError, match="already locked"):
                            with PIDFileLock(temp_pid_file):
                                pass  # Should not reach here
    else:
        # On Unix-like systems, test the original functionality
        # Acquire first lock
        with PIDFileLock(temp_pid_file):
            # Try to acquire second lock
            with pytest.raises(RuntimeError, match="already locked"):
                with PIDFileLock(temp_pid_file):
                    pass # Should not reach here


def test_pid_file_lock_concurrent_access_simulation(
    temp_pid_file: Path
) -> None:
    """Simulate concurrent access (this is more of an integration test)."""
    if sys.platform == "win32":
        # On Windows, test with mocked file locking
        # Need to provide side_effect for both locking and unlocking calls
        # The sequence is: first lock (success), second lock (fail with BlockingIOError)
        # When second lock fails, it doesn't reach the __exit__ method,
        # but first context manager will still try to unlock
        with patch("msvcrt.locking") as mock_locking:
            # First context: lock succeeds, then unlock happens when exiting
            # Second context: lock fails with BlockingIOError (no unlock call since __enter__ fails)
            # Total sequence: lock1, lock2(fail), unlock1
            mock_locking.side_effect = [None, BlockingIOError(), None]  # First lock, second lock (should fail), first unlock
            with patch("os.open", return_value=123):
                with patch("os.close"):
                    # Process 1 acquires the lock
                    lock1 = PIDFileLock(temp_pid_file)
                    
                    # Process 1 enters the lock
                    with lock1:
                        assert lock1._locked is True
                        
                        # Process 2 tries to acquire the lock and should fail
                        lock2 = PIDFileLock(temp_pid_file)
                        with pytest.raises(RuntimeError, match="already locked"):
                            with lock2:
                                pass # Should not reach here
    else:
        # On Unix-like systems, test the original functionality
        # This test simulates what happens if two processes try to lock the same file
        # Process 1 acquires the lock
        lock1 = PIDFileLock(temp_pid_file)
        
        # Process 1 enters the lock
        with lock1:
            assert lock1._locked is True
            
            # Process 2 tries to acquire the lock and should fail
            lock2 = PIDFileLock(temp_pid_file)
            with pytest.raises(RuntimeError, match="already locked"):
                with lock2:
                    pass # Should not reach here


def test_is_pid_running_with_psutil_active_process() -> None:
    """Test is_pid_running with an active process using psutil."""
    with patch.dict('sys.modules', {'psutil': MagicMock()}):
        import sys
        psutil_mock = sys.modules['psutil']
        
        # Mock process that is running
        mock_process = MagicMock()
        mock_process.is_running.return_value = True
        mock_process.status.return_value = 'running'
        
        psutil_mock.Process.return_value = mock_process
        psutil_mock.STATUS_ZOMBIE = 'zombie'
        
        result = is_pid_running(1234)
        assert result is True
        psutil_mock.Process.assert_called_once_with(1234)
        mock_process.is_running.assert_called_once()


def test_is_pid_running_with_psutil_zombie_process() -> None:
    """Test is_pid_running with a zombie process using psutil."""
    with patch.dict('sys.modules', {'psutil': MagicMock()}):
        import sys
        psutil_mock = sys.modules['psutil']
        
        # Mock process that is a zombie
        mock_process = MagicMock()
        mock_process.is_running.return_value = True
        mock_process.status.return_value = 'zombie'
        
        psutil_mock.Process.return_value = mock_process
        psutil_mock.STATUS_ZOMBIE = 'zombie'
        
        result = is_pid_running(1234)
        assert result is False  # Zombie processes should return False


def test_is_pid_running_with_psutil_no_such_process() -> None:
    """Test is_pid_running when process doesn't exist using psutil."""
    with patch.dict('sys.modules', {'psutil': MagicMock()}):
        import sys
        psutil_mock = sys.modules['psutil']
        
        # Create a mock NoSuchProcess exception
        class MockNoSuchProcess(Exception):
            pass
        
        psutil_mock.NoSuchProcess = MockNoSuchProcess
        psutil_mock.AccessDenied = Exception
        
        # Mock Process to raise NoSuchProcess
        mock_process_instance = MagicMock()
        psutil_mock.Process.side_effect = psutil_mock.NoSuchProcess("No such process")
        
        result = is_pid_running(1234)
        assert result is False


def test_is_pid_running_with_psutil_access_denied() -> None:
    """Test is_pid_running when access is denied using psutil."""
    with patch.dict('sys.modules', {'psutil': MagicMock()}):
        import sys
        psutil_mock = sys.modules['psutil']
        
        # Create a mock AccessDenied exception
        class MockAccessDenied(Exception):
            pass
        
        psutil_mock.AccessDenied = MockAccessDenied
        psutil_mock.NoSuchProcess = Exception
        
        # Mock Process to raise AccessDenied
        psutil_mock.Process.side_effect = psutil_mock.AccessDenied("Access denied")
        
        result = is_pid_running(1234)
        assert result is False


def test_is_pid_running_without_psutil_unix() -> None:
    """Test is_pid_running without psutil on Unix-like systems."""
    if sys.platform == "win32":
        pytest.skip("Unix-specific test")
    
    def import_side_effect(name, *args, **kwargs):
        if name == 'psutil':
            raise ImportError
        return __import__(name, *args, **kwargs)
    
    with patch('builtins.__import__', side_effect=import_side_effect):
        # Mock os.kill to simulate process exists
        with patch('os.kill', return_value=None):
            result = is_pid_running(1234)
            assert result is True
            os.kill.assert_called_once_with(1234, 0)


def test_is_pid_running_without_psutil_unix_no_process() -> None:
    """Test is_pid_running without psutil when process doesn't exist on Unix."""
    if sys.platform == "win32":
        pytest.skip("Unix-specific test")
    
    def import_side_effect(name, *args, **kwargs):
        if name == 'psutil':
            raise ImportError
        return __import__(name, *args, **kwargs)
    
    with patch('builtins.__import__', side_effect=import_side_effect):
        # Mock os.kill to raise OSError (process doesn't exist)
        with patch('os.kill', side_effect=OSError("No such process")):
            result = is_pid_running(1234)
            assert result is False
            os.kill.assert_called_once_with(1234, 0)


def test_is_pid_running_without_psutil_windows() -> None:
    """Test is_pid_running without psutil on Windows."""
    if sys.platform != "win32":
        pytest.skip("Windows-specific test")
    
    with patch.dict('sys.modules', {'psutil': None}):
        # On Windows without psutil, the function returns True
        result = is_pid_running(1234)
        assert result is True


def test_check_pid_file_status_nonexistent_file(temp_pid_file: Path) -> None:
    """Test check_pid_file_status when PID file doesn't exist."""
    exists, pid = check_pid_file_status(temp_pid_file)
    assert exists is False
    assert pid is None


def test_check_pid_file_status_invalid_content(temp_pid_file: Path) -> None:
    """Test check_pid_file_status when PID file has invalid content."""
    temp_pid_file.write_text("invalid_content")
    
    exists, pid = check_pid_file_status(temp_pid_file)
    assert exists is True  # File exists
    assert pid is None     # But content is not a valid PID


def test_check_pid_file_status_empty_file(temp_pid_file: Path) -> None:
    """Test check_pid_file_status when PID file is empty."""
    temp_pid_file.write_text("")
    
    exists, pid = check_pid_file_status(temp_pid_file)
    assert exists is True  # File exists
    assert pid is None     # But content is not a valid PID


def test_check_pid_file_status_running_process(temp_pid_file: Path) -> None:
    """Test check_pid_file_status when PID file has valid PID of running process."""
    # Write a valid PID to the file
    temp_pid_file.write_text("1234")
    
    # Mock is_pid_running to return True
    with patch('metaexpert.cli.process.pid_lock.is_pid_running', return_value=True):
        exists, pid = check_pid_file_status(temp_pid_file)
        assert exists is True
        assert pid == 1234


def test_check_pid_file_status_zombie_process(temp_pid_file: Path) -> None:
    """Test check_pid_file_status when PID file has valid PID of non-running process."""
    # Write a valid PID to the file
    temp_pid_file.write_text("1234")
    
    # Mock is_pid_running to return False
    with patch('metaexpert.cli.process.pid_lock.is_pid_running', return_value=False):
        exists, pid = check_pid_file_status(temp_pid_file)
        assert exists is True  # File exists
        assert pid is None     # But process is not running


def test_pid_file_lock_creates_and_writes_pid(temp_pid_file: Path) -> None:
    """Test that PIDFileLock can be used to create PID file with current process ID."""
    # This test verifies that the file is created when used with PIDFileLock
    import os
    
    with PIDFileLock(temp_pid_file):
        # The file should exist after lock acquisition
        assert temp_pid_file.exists()
        # But the PID is not written by PIDFileLock itself, it's done by the caller
        # PIDFileLock only creates an exclusive lock on the file


def test_pid_file_lock_with_existing_pid_file(temp_pid_file: Path) -> None:
    """Test that PIDFileLock handles existing PID files properly."""
    # Create a PID file with some content
    temp_pid_file.write_text("1234")
    
    # This should work fine as PIDFileLock uses O_TRUNC which overwrites the file
    with PIDFileLock(temp_pid_file):
        assert temp_pid_file.exists()
        # At this point, the file is locked and truncated but not yet written to


def test_pid_file_lock_windows_missing_attributes() -> None:
    """Test PIDFileLock behavior when Windows msvcrt attributes are missing."""
    if sys.platform != "win32":
        pytest.skip("Windows-specific test")
    
    # Mock the _lock_windows method to simulate missing attributes
    with patch.object(PIDFileLock, '_lock_windows', side_effect=RuntimeError("Windows file locking not available, msvcrt attributes missing")):
        with patch('os.open', return_value=123):  # Mock file descriptor
            with patch('os.close') as mock_close:
                lock = PIDFileLock(Path("test.pid"))
                
                # This should raise RuntimeError due to missing attributes
                with pytest.raises(RuntimeError, match="Windows file locking not available"):
                    with lock:
                        pass  # Should not reach here
                mock_close.assert_called_once_with(123)


def test_context_manager_proper_cleanup_on_exception(temp_pid_file: Path) -> None:
    """Test that PIDFileLock properly cleans up resources even if an exception occurs."""
    if sys.platform == "win32":
        # On Windows, test the Windows locking mechanism
        with patch("msvcrt.locking") as mock_locking:
            with patch("os.close") as mock_close:
                lock = PIDFileLock(temp_pid_file)
                fd = None
                try:
                    with lock as l:
                        fd = l.fd
                        # Simulate an exception inside the context
                        raise ValueError("Test exception")
                except ValueError:
                    pass  # Expected
                
                # Ensure os.close was called to clean up the file descriptor
                mock_close.assert_called_once_with(fd)
                assert lock.fd is None
    else:
        # On Unix-like systems, test the Unix locking mechanism
        with patch("fcntl.flock") as mock_flock:
            with patch("os.close") as mock_close:
                lock = PIDFileLock(temp_pid_file)
                fd = None
                try:
                    with lock as l:
                        fd = l.fd
                        # Simulate an exception inside the context
                        raise ValueError("Test exception")
                except ValueError:
                    pass  # Expected
                
                # Ensure os.close was called to clean up the file descriptor
                mock_close.assert_called_once_with(fd)
                assert lock.fd is None