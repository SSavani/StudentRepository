#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

HW10 : Test Stevens Repo
Author: Savani Shivam
Date: 11/10/2019 2:00pm

"""
import unittest
from HW10_Shivam_Savani import Student, Instructor, Repository, Major


class TestStevensRepo(unittest.TestCase):
    """Test class to test all the functions"""

    def test_read_student(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        self.assertEqual(10, len(repo.all_students))

    def test_read_major(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        self.assertEqual(2, len(repo.all_majors))

    def test_read_instructor(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        self.assertEqual(6, len(repo.all_instructors))

    def test_read_grade(self):
        path = "C:\\Users\shiva\Desktop\HW10\HW10test"
        with self.assertRaises(ValueError):
            repo = Repository(path)

        path = "C:\\Users\shiva\Desktop\HW10"
        repo1 = Repository(path)
        stud = repo1.all_students.get("10115")
        self.assertEqual(4, len(stud.courses.values()))

    def test_student_addcourse(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        stud = repo.all_students.get("10115")
        self.assertEqual(4, len(stud.courses))

    def test_instructor_addcourse(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        inst = repo.all_instructors.get("98765")
        self.assertEqual(2, len(inst.courses))

    def test_major_addmajor(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        req = repo.all_majors.get("SYEN").req
        self.assertEqual(3, len(req))

    def test_get_major_info(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        majors = repo.all_majors.get("SFEN")
        sfen = ['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']]
        self.assertEqual(majors.get_major_info(), sfen)

    def test_get_instructor_info(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        inst = repo.all_instructors.get("98765")
        einstein = [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3]]
        self.assertEqual(inst.get_instructor_info(), einstein)


    def test_completed_courses(self):
        path = "C:\\Users\shiva\Desktop\HW10"
        repo = Repository(path)
        courses = repo.all_students.get("10115").courses
        comp, req, elect = repo.all_majors["SFEN"].completed_courses(courses)
        self.assertEqual(comp, ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'])
        self.assertEqual(req, {'SSW 540', 'SSW 555'})
        self.assertEqual(elect, None)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)