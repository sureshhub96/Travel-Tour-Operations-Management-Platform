def test_daily_booking_report(client):

    response = client.get(
        "/reports/daily-bookings"
    )

    assert response.status_code == 200


def test_monthly_revenue_report(client):

    response = client.get(
        "/reports/monthly-revenue",
        params={
            "year": 2026,
            "month": 8
        }
    )

    assert response.status_code == 200


def test_destination_revenue_report(client):

    response = client.get(
        "/reports/destination-revenue"
    )

    assert response.status_code == 200


def test_package_performance_report(client):

    response = client.get(
        "/reports/package-performance"
    )

    assert response.status_code == 200