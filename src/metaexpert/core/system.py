"""MetaProcess class for managing trading system processes."""

from logging import Logger
from typing import Self

from metaexpert.config import APP_NAME
from metaexpert.logger import get_logger
from .event_type import EventType
from ..exchanges import MetaExchange

logger: Logger = get_logger(APP_NAME)


class MetaProcess:
    """A high-level process manager for the trading system.
    
    This class provides a simplified interface for managing processes
    in the MetaExpert trading system. It wraps the lower-level Process
    enum and provides additional functionality for process control.
    """

    def __init__(
            self,
            client: MetaExchange,
            name: str = "MetaProcess",
            auto_start: bool = False,
            max_processes: int = 100,
            rate_limit: int = 1200,
            enable_metrics: bool = True,
            persist_state: bool = True,
            state_file: str = "state.json"
    ) -> None:
        """Initialize the MetaProcess manager.
        
        Args:
            client: The exchange client instance.
            name: The name of this process manager instance.
            auto_start: Whether to automatically start the process manager.
            max_processes: Maximum number of processes that can be registered.
            rate_limit: Maximum requests per minute.
            enable_metrics: Whether to enable performance metrics.
            persist_state: Whether to persist state between runs.
            state_file: State persistence file.
        """
        self.client = client
        self.name = name
        self.rate_limit = rate_limit
        self.enable_metrics = enable_metrics
        self.persist_state = persist_state
        self.state_file = state_file
        self.max_processes = max_processes
        self._processes: dict[str, EventType] = {}
        self._is_running: bool = False

        if auto_start:
            self.start()

        logger.debug("MetaProcess manager '%s' initialized", name)

    @classmethod
    def create(
            cls,
            client: MetaExchange,
            name: str = "MetaProcess",
            auto_start: bool = False,
            max_processes: int = 100,
            rate_limit: int = 1200,
            enable_metrics: bool = True,
            persist_state: bool = True,
            state_file: str = "state.json"
    ) -> Self:
        """Create a new MetaProcess instance.
        
        Args:
            client: The exchange client instance.
            name: The name of this process manager instance.
            auto_start: Whether to automatically start the process manager.
            max_processes: Maximum number of processes that can be registered.
            rate_limit: Maximum requests per minute.
            enable_metrics: Whether to enable performance metrics.
            persist_state: Whether to persist state between runs.
            state_file: State persistence file.
            
        Returns:
            Self: A new MetaProcess instance.
        """
        return cls(
            client=client,
            name=name,
            auto_start=auto_start,
            max_processes=max_processes,
            rate_limit=rate_limit,
            enable_metrics=enable_metrics,
            persist_state=persist_state,
            state_file=state_file
        )

    def register_process(self, name: str, process: EventType) -> bool:
        """Register a process with the manager.
        
        Args:
            name: The name to register the process under.
            process: The Process enum instance to register.
            
        Returns:
            bool: True if registration was successful, False otherwise.
        """
        if len(self._processes) >= self.max_processes:
            logger.warning(
                "Cannot register process '%s': maximum process limit (%d) reached",
                name,
                self.max_processes
            )
            return False

        self._processes[name] = process
        logger.debug("Registered process '%s' with manager '%s'", name, self.name)
        return True

    def get_process(self, name: str) -> EventType | None:
        """Get a registered process by name.
        
        Args:
            name: The name of the process to retrieve.
            
        Returns:
            EventType | None: The Process instance if found, otherwise None.
        """
        return self._processes.get(name)

    def start(self) -> None:
        """Start the process manager."""
        if not self._is_running:
            self._is_running = True
            logger.info("MetaProcess manager '%s' started", self.name)

    def stop(self) -> None:
        """Stop the process manager."""
        if self._is_running:
            self._is_running = False
            logger.info("MetaProcess manager '%s' stopped", self.name)

    def is_running(self) -> bool:
        """Check if the process manager is running.
        
        Returns:
            bool: True if running, False otherwise.
        """
        return self._is_running

    def run_process(self, name: str) -> bool:
        """Run a specific registered process.
        
        Args:
            name: The name of the process to run.
            
        Returns:
            bool: True if the process was run successfully, False otherwise.
        """
        process = self.get_process(name)
        if process:
            try:
                process.run()
                logger.debug("Process '%s' executed successfully", name)
                return True
            except Exception as e:
                logger.error("Error running process '%s': %s", name, e)
                return False
        else:
            logger.warning("Process '%s' not found", name)
            return False

    def initialize_processes(self) -> None:
        """Initialize all processes.
        
        This method should be called to set up all registered processes.
        """
        logger.info("Initializing all processes in manager '%s'", self.name)
        # This would typically involve calling init methods on processes
        # For now, we'll just log that initialization is happening
        pass

    def cleanup(self) -> None:
        """Clean up resources used by the process manager."""
        logger.info("Cleaning up MetaProcess '%s' resources", self.name)
        self._processes.clear()
        self.stop()
