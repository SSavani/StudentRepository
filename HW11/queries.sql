--4.1 What is the name of the instructor with CWID='98763'
select Name from instructors where CWID='98763';

-- 4.2 What is the total number of instructors by department?
select Dept, count(*) as Instructors_by_Dept from instructors group by Dept;

-- 4.3 What is the most frequent grade across all students and courses?
select max(Grade) as Most_Freq_Grade from grades group by Grade LIMIT 1;

--4.4  Show the student's name, CWID, and major along with the courses and grades
-- each student received in that course for all grades.
select students.Name, students.CWID, students.Major, grades.Course, grades.Grade
from students JOIN grades on CWID = StudentCWID;

-- 4.5 Show the names of students  who have grades for  'SSW 810'.
select students.Name
from students JOIN grades on CWID = StudentCWID where Course = "SSW 810";


-- 4.6 Recreate the Instructor summary table from HW10, including the Instructor's CWID, name, department,
-- course taught, and the number of students who took the course
select instructors.CWID, instructors.Name, instructors.Dept, grades.Course, COUNT(grades.StudentCWID) as Num_Students
from instructors join grades on CWID = InstructorCWID group by CWID,Course order by CWID DESC, Num_Students DESC ;

