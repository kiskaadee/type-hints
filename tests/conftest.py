import pytest
import revex.core.services.paths
import revex.core.services.config
import revex.core.services.progress
import revex.core.services.setup
import revex.core.services.sync

@pytest.fixture(autouse=True)
def setup_test_environment(tmp_path, monkeypatch):
    """Fixture to isolate filesystem state for tests by using tmp_path."""
    test_state_dir = tmp_path / ".user_data"
    test_workspace_dir = tmp_path / "workspace"
    test_cache_dir = test_state_dir / ".revex_cache"
    
    test_state_dir.mkdir(exist_ok=True)
    test_workspace_dir.mkdir(exist_ok=True)
    test_cache_dir.mkdir(exist_ok=True)
    
    # Patch paths module
    monkeypatch.setattr(revex.core.services.paths, "STATE_DIR", test_state_dir)
    monkeypatch.setattr(revex.core.services.paths, "WORKSPACE_DIR", test_workspace_dir)
    monkeypatch.setattr(revex.core.services.paths, "CACHE_DIR", test_cache_dir)
    
    # Patch config module
    monkeypatch.setattr(revex.core.services.config, "CONFIG_PATH", test_state_dir / "config.toml")
    monkeypatch.setattr(revex.core.services.config, "STATE_DIR", test_state_dir)
    
    # Patch progress module
    monkeypatch.setattr(revex.core.services.progress, "PROGRESS_PATH", test_state_dir / "progress.json")
    monkeypatch.setattr(revex.core.services.progress, "STATE_DIR", test_state_dir)
    
    # Patch setup module
    monkeypatch.setattr(revex.core.services.setup, "STATE_DIR", test_state_dir)
    monkeypatch.setattr(revex.core.services.setup, "WORKSPACE_DIR", test_workspace_dir)
    monkeypatch.setattr(revex.core.services.setup, "CACHE_DIR", test_cache_dir)
    monkeypatch.setattr(revex.core.services.setup, "PROGRESS_PATH", test_state_dir / "progress.json")
    
    # Patch sync module
    monkeypatch.setattr(revex.core.services.sync, "WORKSPACE_DIR", test_workspace_dir)
