#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

HW12 : Test Stevens Repo
Author: Savani Shivam
Date: 11/19/2019 2:00pm

"""
import unittest
from HW12_Shivam_Savani import Student, Instructor, Repository, Major, instructor_table_db


class TestStevensRepo(unittest.TestCase):
    """Test class to test all the functions"""

    def test_read_student(self):
        """to test read_students function of Repository class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        keys = "dict_keys(['10103', '10115', '10183', '11714', '11717'])"
        self.assertEqual(str(repo.all_students.keys()), keys)

    def test_read_major(self):
        """to test read_major function of Repository class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        keys = "dict_keys(['SFEN', 'CS'])"
        self.assertEqual(str(repo.all_majors.keys()), keys)

    def test_read_instructor(self):
        """to test read_instructor function of Repository class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        keys = "dict_keys(['98764', '98763', '98762'])"
        self.assertEqual(str(repo.all_instructors.keys()), keys)

    def test_read_grade(self):
        """to test read_grade function of Repository class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12\HW12test"
        with self.assertRaises(ValueError):
            repo = Repository(path)

        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo1 = Repository(path)
        stud = repo1.all_students.get("10115")
        grades = "dict_values(['A', 'F'])"
        self.assertEqual(grades, str(stud.courses.values()))

    def test_student_addcourse(self):
        """to test add_course function of Student class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        stud = repo.all_students.get("10115")
        course_keys = "dict_keys(['SSW 810', 'CS 546'])"
        self.assertEqual(course_keys, str(stud.courses.keys()))

    def test_instructor_addcourse(self):
        """to test add_course function of Instructor class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        inst = repo.all_instructors.get("98762")
        course_keys = "dict_keys(['CS 501', 'CS 546', 'CS 570'])"
        self.assertEqual(course_keys, str(inst.courses.keys()))

    def test_major_addmajor(self):
        """to test add_course function of Major class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        req = repo.all_majors.get("SFEN").req
        req_courses = {'SSW 555', 'SSW 810', 'SSW 540'}
        self.assertEqual(req, req_courses)

        elect = repo.all_majors.get("SFEN").elect
        elect_courses = {'CS 501', 'CS 546'}
        self.assertEqual(elect, elect_courses)

    def test_get_major_info(self):
        """to test get_major_info function of Major class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        majors = repo.all_majors.get("SFEN")
        sfen = ['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']]
        self.assertEqual(majors.get_major_info(), sfen)

    def test_get_instructor_info(self):
        """to test get_instructor_info function of Instructor class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        inst = repo.all_instructors.get("98762")
        hawking = [['98762', 'Hawking, S', 'CS', 'CS 501', 1], ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]
        self.assertEqual(inst.get_instructor_info(), hawking)


    def test_completed_courses(self):
        """to test completed_courses function of Major class which indirectly tests remaining_req and remaining_elect
        functions of Major class"""
        path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
        repo = Repository(path)
        courses = repo.all_students.get("10115").courses
        comp, req, elect = repo.all_majors["SFEN"].completed_courses(courses)
        test_comp = ['SSW 810']             # Completed Courses
        test_req = {'SSW 540', 'SSW 555'}   # Remaining Required Courses
        test_elect = {'CS 546', 'CS 501'}   # Remaining Elective Courses
        self.assertEqual(comp, test_comp)
        self.assertEqual(req, test_req)
        self.assertEqual(elect, test_elect)

    # def test_db_instructor_summary(self):
    #     """To test the data retrieved from the database matches the expected rows."""
    #     db_path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12\stevens.db"
    #     path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW12"
    #     repo = Repository(path)
    #     pt_expected = repo.instructor_prettytable()
    #     pt_inst_db = instructor_table_db().su\\
    #     self.assertEqual(str(pt_expected), str(pt_inst_db))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)