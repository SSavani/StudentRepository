#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

HW09 : Stevens Repo
Author: Savani Shivam
Date: 10/29/2019 2:00pm

"""

import os
from prettytable import PrettyTable
from collections import defaultdict


class Student:
    """Student class to store student details"""

    def __init__(self, cwid, name, major):
        if cwid.strip() == "" or name.strip() == "" or major.strip() == "":
            raise ValueError(f"One of the (Cwid, name, major) arguments' value is missing (Cannot be empty) ")
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = defaultdict(str)

    def add_course(self, course, grade=None):
        """Add courses the student has enrolled in"""
        if grade.strip() == "":
            grade = None
        self.courses[course] = grade

    def get_student_info(self):
        """get info for a single student"""
        if self.courses.items():

            return [self.cwid, self.name, self.major, sorted(self.courses.keys())]
        else:
            return [self.cwid, self.name, self.major, None]


class Instructor:
    """Class to store details of insturctors"""

    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses = defaultdict(int)

    def add_course(self, course):
        """To add courses the instructor is teaching and num of students enrolled in it"""
        self.courses[course] += 1

    def get_instructor_info(self):
        """Get all info for a single instructor """
        instruct_info = []
        if self.courses.items():
            for course, stud_num in self.courses.items():
                instruct_info.append([self.cwid, self.name, self.dept, course, stud_num])
        else:
            instruct_info.append([self.cwid, self.name, self.dept, None, None])
        return instruct_info


class Repository:
    """Class to store all instances of students, instructors and grades"""

    def __init__(self, dir_path):
        os.chdir(dir_path)
        self.dir_path = dir_path
        self.students_filepath = os.path.join(dir_path, "students.txt")
        self.instructors_filepath = os.path.join(dir_path, "instructors.txt")
        self.grades_filepath = os.path.join(dir_path, "grades.txt")

        self.all_students = {}
        self.all_instructors = {}

        self.read_files()  # call all read functions
        self.print_pt()  # call to print summary of students and instructors

    def read_files(self):
        """Function call To read files """
        self.read_students()
        self.read_instructors()
        self.read_grades()

    def print_pt(self):
        """Function call to print summary"""
        self.student_prettytable()
        self.instructor_prettytable()

    def file_reading_gen(self, filepath):
        """generator function to read tab separated text files and yield a list with all of the values
        from a single line in the file on each call to next()"""

        try:
            fp = open(filepath)
        except FileNotFoundError:
            print("Error: Cannot Open File at", filepath)
        else:
            with fp:
                for line in fp:
                    yield line.rstrip("\n").split("\t")

    def read_students(self):
        """Read students.txt and store the (Key:CWID) and (Value:instance of Student class) in the dictionary"""
        for student in self.file_reading_gen(self.students_filepath):
            cwid, name, major = student
            if cwid not in self.all_students:
                self.all_students[cwid] = Student(cwid, name, major)

    def read_instructors(self):
        """Read instructors.txt and store the (Key:CWID) and (Value:instance of Instructor class) in the dictionary"""
        for instructor in self.file_reading_gen(self.instructors_filepath):
            cwid, name, dept = instructor
            if cwid not in self.all_instructors:
                self.all_instructors[cwid] = Instructor(cwid, name, dept)

    def read_grades(self):
        """Read grades.txt and update the grade of the course for given student and
        update the count of students enrolled in the course taught by the particular instructor """
        for grade_info in self.file_reading_gen(self.grades_filepath):
            stud_cwid, course, grade, inst_cwid = grade_info
            if stud_cwid in self.all_students.keys():
                self.all_students[stud_cwid].add_course(course, grade)
            else:
                raise ValueError(f"CWID: {stud_cwid} of student not present in students database ")

            if inst_cwid in self.all_instructors.keys():
                self.all_instructors[inst_cwid].add_course(course)
            else:
                raise ValueError(f"CWID: {inst_cwid} of instructor not present in instructors database ")

    def student_prettytable(self):
        """Print summary of students"""
        pt = PrettyTable(field_names=["CWID", "Name", "Completed Courses"])
        for student in self.all_students.values():
            cwid, name, major, courses = student.get_student_info()
            pt.add_row([cwid, name, courses])

        print("\nStudent Summary")
        print(pt)

    def instructor_prettytable(self):
        """Print summary of Instructors"""
        pt = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for instructor in self.all_instructors.values():
            for info in instructor.get_instructor_info():
                pt.add_row(info)

        print("\nInstructor Summary")
        print(pt)


def main():
    path = "C:\\Users\shiva\Desktop\hw9"
    try:
        repo_stevens = Repository(path)
    except ValueError:
        print("Error", ValueError)
    except Exception:
        print("Exception", Exception)


if __name__ == "__main__":
    main()
