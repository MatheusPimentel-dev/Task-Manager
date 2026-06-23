import unittest

from app import create_app
from app.extensions import db
from app.models.task import Task


class TaskRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _create_task(self):
        with self.app.app_context():
            task = Task(
                title="Teste",
                importance=5,
                urgency=4,
                duration=30,
                weight=14,
                scheduled_time="2026-06-22 09:00",
                fixed=False,
                days_of_week=None,
                done=False,
                deleted=False,
                notification_sent=False,
            )
            db.session.add(task)
            db.session.commit()
            return task.id

    def test_create_valid_task(self):
        response = self.client.post(
            "/tasks/",
            data={
                "title": "Nova",
                "importance": "8",
                "urgency": "7",
                "duration": "25",
                "scheduled_time": "2026-06-22T10:00",
            },
        )

        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            task = Task.query.one()
            self.assertEqual(task.title, "Nova")
            self.assertEqual(task.scheduled_time, "2026-06-22 10:00")
            self.assertEqual(task.weight, 23)

    def test_reject_invalid_task_create(self):
        response = self.client.post(
            "/tasks/",
            data={
                "title": "Invalida",
                "importance": "11",
                "urgency": "7",
                "duration": "25",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_edit_existing_task(self):
        task_id = self._create_task()

        response = self.client.post(
            f"/tasks/edit/{task_id}",
            data={
                "title": "Editada",
                "importance": "3",
                "urgency": "2",
                "duration": "45",
                "scheduled_time": "2026-06-22T11:00",
                "fixed": "1",
                "days_of_week": ["0", "2"],
            },
        )

        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            task = db.session.get(Task, task_id)
            self.assertEqual(task.title, "Editada")
            self.assertTrue(task.fixed)
            self.assertEqual(task.days_of_week, "0,2")
            self.assertEqual(task.weight, 8)

    def test_complete_via_post(self):
        task_id = self._create_task()

        response = self.client.post(f"/tasks/complete/{task_id}")

        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            self.assertTrue(db.session.get(Task, task_id).done)

    def test_delete_via_post(self):
        task_id = self._create_task()

        response = self.client.post(f"/tasks/delete/{task_id}")

        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            self.assertTrue(db.session.get(Task, task_id).deleted)

    def test_complete_and_delete_get_do_not_mutate(self):
        task_id = self._create_task()

        complete_response = self.client.get(f"/tasks/complete/{task_id}")
        delete_response = self.client.get(f"/tasks/delete/{task_id}")

        self.assertEqual(complete_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)
        with self.app.app_context():
            task = db.session.get(Task, task_id)
            self.assertFalse(task.done)
            self.assertFalse(task.deleted)


if __name__ == "__main__":
    unittest.main()
