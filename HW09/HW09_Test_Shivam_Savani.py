#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

HW09 : Test Stevens Repo
Author: Savani Shivam
Date: 10/29/2019 2:00pm

"""
import unittest
from HW09_Shivam_Savani import Student, Instructor, Repository


class TestStevensRepo(unittest.TestCase):
    """Test class to test all the functions"""

    def test_read_student(self):
        path = "C:\\Users\shiva\Desktop\hw9"
        repo = Repository(path)
        self.assertEqual(10, len(repo.all_students))

    def test_read_instructor(self):
        path = "C:\\Users\shiva\Desktop\hw9"
        repo = Repository(path)
        self.assertEqual(6, len(repo.all_instructors))

    def test_read_grade(self):
        path = "C:\\Users\shiva\Desktop\hw9\hw9test"
        with self.assertRaises(ValueError):
            repo = Repository(path)

        path = "C:\\Users\shiva\Desktop\hw9"
        repo1 = Repository(path)
        stud = repo1.all_students.get("10115")
        self.assertEqual(4, len(stud.courses.values()))

    def test_student_addcourse(self):
        path = "C:\\Users\shiva\Desktop\hw9"
        repo = Repository(path)
        stud = repo.all_students.get("10115")
        self.assertEqual(4, len(stud.courses))

    def test_instructor_addcourse(self):
        path = "C:\\Users\shiva\Desktop\hw9"
        repo = Repository(path)
        inst = repo.all_instructors.get("98765")
        self.assertEqual(2, len(inst.courses))

    def test_get_student_info(self):
        path = "C:\\Users\shiva\Desktop\hw9"
        repo = Repository(path)
        stud = repo.all_students.get("10115")
        wyatt = ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']]
        self.assertEqual(stud.get_student_info(), wyatt)

    def test_get_instructor_info(self):
        path = "C:\\Users\shiva\Desktop\hw9"
        repo = Repository(path)
        inst = repo.all_instructors.get("98765")
        einstein = [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3]]
        self.assertEqual(inst.get_instructor_info(), einstein)


if __name__ == '__main__':
    unittest.main()
