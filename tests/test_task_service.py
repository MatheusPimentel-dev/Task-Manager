import unittest
from datetime import datetime
from unittest.mock import patch

from app.services.task_service import TaskService


class TaskServiceTestCase(unittest.TestCase):
    def test_calculate_priority(self):
        self.assertEqual(TaskService._calculate_priority(4, 3), 11)

    @patch.object(TaskService, "list_fixed_tasks", return_value=[])
    @patch.object(TaskService, "free_slots")
    @patch.object(TaskService, "list_normal_tasks")
    def test_list_ordered_normal_tasks_by_weight(self, list_normal_tasks, free_slots, _list_fixed_tasks):
        list_normal_tasks.return_value = [
            {"id": 1, "title": "Baixa", "weight": 1, "duration": 30},
            {"id": 2, "title": "Alta", "weight": 10, "duration": 30},
        ]
        free_slots.return_value = [
            (datetime(2026, 6, 22, 9, 0), datetime(2026, 6, 22, 10, 0)),
        ]

        tasks = TaskService.list_ordered_normal_tasks()

        self.assertEqual([task["id"] for task in tasks], [2, 1])
        self.assertEqual(tasks[0]["scheduled_time"], "2026-06-22 09:00")
        self.assertEqual(tasks[1]["scheduled_time"], "2026-06-22 09:30")

    def test_get_fixed_blocks_for_current_day(self):
        tasks = [
            {
                "days_of_week": "0,2",
                "scheduled_time": "2026-06-22 08:00",
                "duration": 60,
            },
            {
                "days_of_week": "1",
                "scheduled_time": "2026-06-23 09:00",
                "duration": 30,
            },
        ]

        blocks = TaskService.get_fixed_blocks(tasks, current_day=0)

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0][0], datetime(2026, 6, 22, 8, 0))
        self.assertEqual(blocks[0][1], datetime(2026, 6, 22, 9, 0))

    def test_find_free_slots(self):
        start_day = datetime(2026, 6, 22, 8, 0)
        end_day = datetime(2026, 6, 22, 12, 0)
        blocks = [
            (datetime(2026, 6, 22, 9, 0), datetime(2026, 6, 22, 10, 0)),
            (datetime(2026, 6, 22, 11, 0), datetime(2026, 6, 22, 11, 30)),
        ]

        slots = TaskService.find_free_slots(blocks, start_day, end_day)

        self.assertEqual(
            slots,
            [
                (datetime(2026, 6, 22, 8, 0), datetime(2026, 6, 22, 9, 0)),
                (datetime(2026, 6, 22, 10, 0), datetime(2026, 6, 22, 11, 0)),
                (datetime(2026, 6, 22, 11, 30), datetime(2026, 6, 22, 12, 0)),
            ],
        )

    @patch.object(TaskService, "list_fixed_tasks", return_value=[])
    @patch.object(TaskService, "free_slots")
    @patch.object(TaskService, "list_normal_tasks")
    def test_task_that_does_not_fit_is_not_scheduled(self, list_normal_tasks, free_slots, _list_fixed_tasks):
        list_normal_tasks.return_value = [
            {"id": 1, "title": "Longa", "weight": 10, "duration": 90},
        ]
        free_slots.return_value = [
            (datetime(2026, 6, 22, 9, 0), datetime(2026, 6, 22, 10, 0)),
        ]

        self.assertEqual(TaskService.list_ordered_normal_tasks(), [])


if __name__ == "__main__":
    unittest.main()
