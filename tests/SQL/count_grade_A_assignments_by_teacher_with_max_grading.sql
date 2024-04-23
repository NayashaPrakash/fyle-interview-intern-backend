-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

WITH TeacherGrades AS (
    SELECT teacher_id,
           COUNT(*) AS graded_count
    FROM assignments
    WHERE grade IS NOT NULL
    GROUP BY teacher_id
    ORDER BY graded_count DESC, teacher_id  -- Additional sorting to ensure consistency
),
MaxGrades AS (
    SELECT MAX(graded_count) AS max_graded
    FROM TeacherGrades
)
SELECT COUNT(*) AS grade_A_count
FROM assignments
JOIN TeacherGrades ON assignments.teacher_id = TeacherGrades.teacher_id
WHERE assignments.grade = 'A'
  AND TeacherGrades.graded_count = (SELECT max_graded FROM MaxGrades);
