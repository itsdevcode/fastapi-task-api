from unittest.mock import Mock, patch
import pytest
import services.task as service

def test_create_task_success():
    #ARRANGE (PREPARE)
    fake_db = Mock()
    fake_task_input = Mock()
    fake_created_task = Mock()

    with patch( 
        "services.task.task_repository.create_task",
        return_value=fake_created_task
    ) as mock_create:
        #ACT
        result = service.create(fake_task_input,fake_db)

        #Assert
        mock_create.assert_called_once_with(fake_task_input, fake_db)
        fake_db.commit.assert_called_once()

        fake_db.refresh.assert_called_once_with(fake_created_task)
        assert result == fake_created_task

def test_create_task_failure():
    fake_db = Mock()
    fake_task_input = Mock()
    
    with patch(
        "services.task.task_repository.create_task",
        side_effect=Exception("Database error")
    ) as mock_create:
        # Act
        with pytest.raises(Exception):
            service.create(fake_task_input, fake_db)
            
        # Assert
        mock_create.assert_called_once_with(fake_task_input, fake_db)
        fake_db.rollback.assert_called_once()

def test_create_task_commit_failure():
    fake_db = Mock()
    fake_task_input = Mock()
    fake_created_task = Mock()
    
    # db.commit() par exception throw karwana hai
    fake_db.commit.side_effect = Exception("Commit error")
    
    with patch(
        "services.task.task_repository.create_task",
        return_value=fake_created_task
    ) as mock_create:
        # Act
        with pytest.raises(Exception):
            service.create(fake_task_input, fake_db)
            
        # Assert
        mock_create.assert_called_once_with(fake_task_input, fake_db)

        
        fake_db.commit.assert_called_once()
        fake_db.rollback.assert_called_once()
        fake_db.refresh.assert_not_called()