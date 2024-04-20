from rest_framework import status
from rest_framework.test import APITestCase


class CommentListTestCase(APITestCase):
    def test_get_comment_list(self):
        url = '/api/comments/1/'  # Замените на фактический URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comment(self):
        url = '/api/comments/1/'  # Замените на фактический URL
        data = {'comment_text': 'Test comment'}  # Пример данных для создания комментария
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentDetailTestCase(APITestCase):
    def test_delete_comment(self):
        comment_id = 1  # Замените на фактический идентификатор комментария для удаления
        url = f'/api/comments/{comment_id}/detail/'  # Замените на фактический URL с идентификатором комментария
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
