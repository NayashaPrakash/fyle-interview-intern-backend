from core.models.assignments import AssignmentStateEnum, GradeEnum

def test_get_teachers(client, h_principal):

    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )
    assert response.status_code == 200

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal, h_student_2):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    draft_response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'content': 'vanilla'
        })

    assert draft_response.status_code == 200
    draft_data = draft_response.json['data']
    draft_id = draft_data['id']

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': draft_id,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )
    assert response.status_code == 400

def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C

def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
