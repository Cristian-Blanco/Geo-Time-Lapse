import ee

class EEInitializer:
    _initialized = False
    _current_project = None

    @classmethod
    def initialize(cls, project_id: str) -> None:
        """
        Singleton initializer for the Earth Engine session,
        skips if already active unless project_id changes.

        Args:
            project_id: Google Cloud project ID for Earth Engine.
        """
        if project_id is None:
            raise ValueError("Project ID cannot be None")

        if cls._initialized and cls._current_project == project_id:
            return

        try:
            ee.Initialize(project=project_id)

            cls._current_project = project_id
            cls._initialized = True

        except Exception as e:
            raise RuntimeError(f"Failed to initialize Google Earth Engine: {e}")
