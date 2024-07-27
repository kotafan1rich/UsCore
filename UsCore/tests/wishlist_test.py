from httpx import AsyncClient


class TestWishList:
    json_create = {
        "priority": 0,
        "text": "Example text",
        "is_finished": False
    }

    json_update = {
        "priority": 2,
        "text": "Example text 2",
        "is_finished": True
    }

    async def test_wishlist_post(self, client):
        response = await client.post("/wishlist/", json=self.json_create)

        assert response.status_code == 200
        data = response.json()
        assert data.get("priority") == 0
        assert data.get("text") == "Example text"
        assert data.get("is_finished") is False

    async def test_wishlist_post_invalid_is_finished(self, client: AsyncClient):
        response = await client.post("/wishlist/", json={
            "priority": 0,
            "text": "Example text",
            "is_finished": 66
        })
        assert response.status_code == 422

    async def test_wishlist_post_invalid_priority(self, client: AsyncClient):
        response = await client.post("/wishlist/", json={
            "priority": -1,
            "text": "Example text",
            "is_finished": True
        })
        assert response.status_code == 422

    async def test_wishlist_get(self, client: AsyncClient):
        response_create = await client.post("/wishlist/", json=self.json_create)

        response_get = await client.get("/wishlist/", params={
            "id": response_create.json().get("id")
        })
        assert response_get.json().get("result")[0] == response_create.json()

    async def test_wishlist_delete(self, client: AsyncClient):
        response_create = await client.post("/wishlist/", json=self.json_create)

        response_delete = await client.delete("/wishlist/", params={
            "id": response_create.json().get("id")
        })
        assert response_delete.status_code == 200
        assert response_delete.json().get("result")[0] == response_create.json()
        response_delete = await client.delete("/wishlist/", params={
            "id": response_create.json().get("id")
        })
        assert response_delete.status_code == 404

    async def test_wishlist_update(self, client: AsyncClient):
        response_create = await client.post("/wishlist/", json=self.json_create)
        response_create_json = response_create.json()

        response_update = await client.patch("/wishlist/", json=self.json_update, params={"id": response_create_json["id"]})

        response_update_json = response_update.json()

        assert response_update.status_code == 200
        assert all([
            response_create_json["id"] == response_update_json["id"],
            response_create_json["create_date"] == response_update_json["create_date"],
            response_update_json["text"] == self.json_update["text"],
            response_update_json["priority"] == self.json_update["priority"],
            response_update_json["is_finished"] == self.json_update["is_finished"]
        ])
