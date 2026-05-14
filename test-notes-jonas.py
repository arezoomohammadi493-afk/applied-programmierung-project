import pytest
import requests
import time
from faker import Faker

name_faker = Faker()

BASE_URL = "http://127.0.0.1:8000"

# Testet, ob die Startseite erreichbar ist und die richtige Begruessung zurueckgibt.
def test_get_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data= response.json()
    assert data["message"] == "Hello World!"


# Testet, ob eine nicht vorhandene Route korrekt den Statuscode 404 zurueckgibt.
def test_check_404_error():
    response = requests.get(f"{BASE_URL}/nonexistent")
    assert response.status_code == 404


# Testet, ob der Greeting-Endpunkt fuer mehrere zufaellige Namen korrekt antwortet.
def test_greetings():
    for _ in range(10):
        name = name_faker.first_name()
        response = requests.get(f"{BASE_URL}/greetings/{name}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Hello {name}!"


# Testet fuer Alter 0 bis 39, ob is_adult, can_drive und can_vote korrekt berechnet werden.
def test_is_adult():
    
    for age in range(0, 40):
        
        adult= age >= 18
        response = requests.get(f"{BASE_URL}/is-adult/{age}")
        
        assert response.status_code == 200
        data = response.json()
        
                    
        for key in ["is_adult", "can_drive", "can_vote"]:
            assert data[key] == adult
        assert data["age"] == age
        

# Testet, ob negative Alterswerte als ungueltig erkannt werden und Statuscode 400 liefern.
def test_is_adult_negative_age():
    
    for age in range(-20, 0):
        
        
        response = requests.get(f"{BASE_URL}/is-adult/{age}")
        assert response.status_code == 400
        
        

##########
### ZUSAETZLICHE TESTS
##########

# Testet, ob die Startseite JSON zurueckgibt und das Feld "message" enthaelt.
def test_root_response_is_json():
    response = requests.get(f"{BASE_URL}/")
    
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert "message" in response.json()


# Testet, ob Namen mit Bindestrich im Greeting-Endpunkt korrekt verarbeitet werden.
def test_greeting_with_hyphen_name():
    name = "Anna-Maria"
    response = requests.get(f"{BASE_URL}/greetings/{name}")
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {name}!"


# Testet, ob Namen mit Leerzeichen per URL-Encoding korrekt verarbeitet werden.
def test_greeting_with_space_in_name():
    name = "Max%20Mustermann"
    expected_name = "Max Mustermann"
    response = requests.get(f"{BASE_URL}/greetings/{name}")
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {expected_name}!"


# Testet den Grenzfall Alter 0: keine Erwachsenenrechte.
def test_is_adult_zero_age_boundary():
    response = requests.get(f"{BASE_URL}/is-adult/0")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 0
    assert data["is_adult"] is False
    assert data["can_vote"] is False
    assert data["can_drive"] is False


# Testet den Grenzfall Alter 17: noch nicht volljaehrig.
def test_is_adult_17_boundary():
    response = requests.get(f"{BASE_URL}/is-adult/17")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 17
    assert data["is_adult"] is False
    assert data["can_vote"] is False
    assert data["can_drive"] is False


# Testet den Grenzfall Alter 18: genau ab hier volljaehrig.
def test_is_adult_18_boundary():
    response = requests.get(f"{BASE_URL}/is-adult/18")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 18
    assert data["is_adult"] is True
    assert data["can_vote"] is True
    assert data["can_drive"] is True


# Testet ein sehr hohes Alter als gueltigen Erwachsenenfall.
def test_is_adult_high_age():
    response = requests.get(f"{BASE_URL}/is-adult/120")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 120
    assert data["is_adult"] is True
    assert data["can_vote"] is True
    assert data["can_drive"] is True


# Testet, ob ein nicht-numerischer Alterswert von FastAPI mit 422 abgelehnt wird.
def test_is_adult_invalid_age_type():
    response = requests.get(f"{BASE_URL}/is-adult/not-a-number")
    
    assert response.status_code == 422


# Testet, ob Gross- und Kleinschreibung im Namen unveraendert zurueckgegeben wird.
def test_greeting_keeps_uppercase_name():
    name = "JONAS"
    response = requests.get(f"{BASE_URL}/greetings/{name}")
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {name}!"


# Testet einen sehr grossen Alterswert als Grenzfall fuer Integer-Parameter.
def test_is_adult_very_high_age():
    response = requests.get(f"{BASE_URL}/is-adult/999")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 999
    assert data["is_adult"] is True
    assert data["can_vote"] is True
    assert data["can_drive"] is True


##########
### PERFORMANCE TESTS
##########

# Testet, ob mehrere Requests schnell genug verarbeitet werden.
def test_is_adult_performance_multiple_requests():
    start_time = time.perf_counter()
    
    for _ in range(50):
        response = requests.get(f"{BASE_URL}/is-adult/18")
        assert response.status_code == 200
    
    duration = time.perf_counter() - start_time
    assert duration < 5.0


# Testet, ob der Root-Endpunkt viele einfache Requests schnell beantwortet.
def test_root_performance_multiple_requests():
    start_time = time.perf_counter()
    
    for _ in range(50):
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
    
    duration = time.perf_counter() - start_time
    assert duration < 5.0


# Testet, ob der Greeting-Endpunkt bei vielen verschiedenen Namen schnell bleibt.
def test_greetings_performance_multiple_names():
    start_time = time.perf_counter()
    
    for i in range(50):
        response = requests.get(f"{BASE_URL}/greetings/TestName{i}")
        assert response.status_code == 200
    
    duration = time.perf_counter() - start_time
    assert duration < 5.0


# Testet, ob viele unterschiedliche Alterswerte schnell verarbeitet werden.
def test_is_adult_performance_many_ages():
    start_time = time.perf_counter()
    
    for age in range(0, 100):
        response = requests.get(f"{BASE_URL}/is-adult/{age}")
        assert response.status_code == 200
    
    duration = time.perf_counter() - start_time
    assert duration < 8.0


# Testet, ob auch Fehlerantworten fuer ungueltige Alterswerte schnell kommen.
def test_invalid_age_performance_multiple_requests():
    start_time = time.perf_counter()
    
    for _ in range(30):
        response = requests.get(f"{BASE_URL}/is-adult/not-a-number")
        assert response.status_code == 422
    
    duration = time.perf_counter() - start_time
    assert duration < 5.0


##########
### 20 WEITERE TESTS FUER MAIN-DAY4.PY
##########

# Testet, ob die Root-Antwort genau das erwartete JSON-Objekt enthaelt.
def test_root_exact_response():
    response = requests.get(f"{BASE_URL}/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


# Testet, ob die Root-Antwort keine unerwarteten Felder enthaelt.
def test_root_only_contains_message_key():
    response = requests.get(f"{BASE_URL}/")
    
    assert response.status_code == 200
    assert list(response.json().keys()) == ["message"]


# Testet, ob mehrere Root-Aufrufe immer dieselbe Antwort liefern.
def test_root_repeated_requests_same_response():
    first_response = requests.get(f"{BASE_URL}/")
    second_response = requests.get(f"{BASE_URL}/")
    
    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json() == second_response.json()


# Testet, ob ein Zahlen-Name im Greeting-Endpunkt korrekt verarbeitet wird.
def test_greeting_numeric_name():
    name = "12345"
    response = requests.get(f"{BASE_URL}/greetings/{name}")
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {name}!"


# Testet, ob ein Name mit Unterstrich korrekt verarbeitet wird.
def test_greeting_name_with_underscore():
    name = "Max_Test"
    response = requests.get(f"{BASE_URL}/greetings/{name}")
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {name}!"


# Testet, ob ein komplett kleingeschriebener Name unveraendert bleibt.
def test_greeting_lowercase_name():
    name = "jonas"
    response = requests.get(f"{BASE_URL}/greetings/{name}")
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {name}!"


# Testet, ob URL-encodete Sonderzeichen im Namen korrekt zurueckgegeben werden.
def test_greeting_encoded_plus_signs():
    response = requests.get(f"{BASE_URL}/greetings/C%2B%2B")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Hello C++!"


# Testet, ob ein sehr langer Name ohne Fehler verarbeitet wird.
def test_greeting_long_name():
    name = "A" * 100
    response = requests.get(f"{BASE_URL}/greetings/{name}")
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {name}!"


# Testet, ob ein fehlender Name beim Greeting-Endpunkt 404 liefert.
def test_greeting_missing_name_returns_404():
    response = requests.get(f"{BASE_URL}/greetings/", allow_redirects=False)
    
    assert response.status_code == 404


# Testet, ob Alter 1 korrekt als minderjaehrig erkannt wird.
def test_is_adult_age_1():
    response = requests.get(f"{BASE_URL}/is-adult/1")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 1
    assert data["is_adult"] is False


# Testet, ob Alter 16 korrekt als minderjaehrig erkannt wird.
def test_is_adult_age_16():
    response = requests.get(f"{BASE_URL}/is-adult/16")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 16
    assert data["can_vote"] is False
    assert data["can_drive"] is False


# Testet, ob Alter 19 korrekt als volljaehrig erkannt wird.
def test_is_adult_age_19():
    response = requests.get(f"{BASE_URL}/is-adult/19")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 19
    assert data["is_adult"] is True


# Testet, ob Alter 65 korrekt als volljaehrig erkannt wird.
def test_is_adult_age_65():
    response = requests.get(f"{BASE_URL}/is-adult/65")
    data = response.json()
    
    assert response.status_code == 200
    assert data["age"] == 65
    assert data["can_vote"] is True
    assert data["can_drive"] is True


# Testet, ob ein stark negativer Alterswert mit 400 abgelehnt wird.
def test_is_adult_negative_100():
    response = requests.get(f"{BASE_URL}/is-adult/-100")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Age cannot be negative"


# Testet, ob eine Kommazahl als Alter mit 422 abgelehnt wird.
def test_is_adult_float_age_returns_422():
    response = requests.get(f"{BASE_URL}/is-adult/18.5")
    
    assert response.status_code == 422


# Testet, ob ein fehlendes Alter beim is-adult-Endpunkt 404 liefert.
def test_is_adult_missing_age_returns_404():
    response = requests.get(f"{BASE_URL}/is-adult/", allow_redirects=False)
    
    assert response.status_code == 404


# Testet, ob POST auf der Root-Route nicht erlaubt ist.
def test_post_root_method_not_allowed():
    response = requests.post(f"{BASE_URL}/")
    
    assert response.status_code == 405


# Testet, ob POST auf dem Greeting-Endpunkt nicht erlaubt ist.
def test_post_greeting_method_not_allowed():
    response = requests.post(f"{BASE_URL}/greetings/Jonas")
    
    assert response.status_code == 405


# Testet, ob POST auf dem is-adult-Endpunkt nicht erlaubt ist.
def test_post_is_adult_method_not_allowed():
    response = requests.post(f"{BASE_URL}/is-adult/18")
    
    assert response.status_code == 405


# Testet, ob ein ungueltiger Pfad unter is-adult nicht versehentlich akzeptiert wird.
def test_is_adult_invalid_nested_path_returns_404():
    response = requests.get(f"{BASE_URL}/is-adult/18/extra")
    
    assert response.status_code == 404
    