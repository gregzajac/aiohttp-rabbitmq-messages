async def test_set_message(client):
    response = await client.post(
        "/api", json={"speed": 20}, headers={"content-type": "application/json"}
    )
    assert response.status == 200
    response_data = await response.json()
    assert response_data["success"] is True
    assert "data" in response_data


async def test_set_message_invalid_content_type(client):
    response = await client.post("/api", data={"speed": 20})
    assert response.status == 415
    response_data = await response.json()
    assert response_data["success"] is False
    assert "data" not in response_data
    assert (
        response_data["message"] == "Invalid Content-Type, must be 'application/json'"
    )


async def test_get_message(client):
    response = await client.get("/api?key=speed")
    assert response.status == 200
    response_data = await response.json()
    assert response_data == {"success": True, "data": 20}


async def test_get_message_not_key_string(client):
    response = await client.get("/api?notkey=speed")
    assert response.status == 400
    response_data = await response.json()
    assert response_data["success"] is False
    assert "data" not in response_data
    assert response_data["message"] == "Acceptable one parameter named 'key'"