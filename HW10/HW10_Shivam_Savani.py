#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

HW10 : Stevens Repo
Author: Savani Shivam
Date: 11/10/2019 2:00pm

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
        self.major = Major(major)
        self.courses = defaultdict(str)

    def add_course(self, course, grade=None):
        """Add courses the student has enrolled in"""
        if grade.strip() == "":
            grade = None
        self.courses[course] = grade

    def get_student_info(self):
        """get info for a single student"""
        if self.courses.items():
            # comp_courses, req_courses, elect_courses = self.major.completed_courses(self.courses)
            return [self.cwid, self.name, self.major, self.courses]
        else:
            return [self.cwid, self.name, self.major, None]


class Major:
    """Major class to store details about courses in a major"""

    def __init__(self, major):
        self.major = major
        self.req = set()
        self.elect = set()

    def add_major(self, req_elec, course):
        """To add the req/elective courses """
        if req_elec != "R" and req_elec != "E":
            raise ValueError("Invalid course type")
        elif req_elec == "R":
            self.req.add(course)
        elif req_elec == "E":
            self.elect.add(course)

    def get_major_info(self):
        """to get major info"""
        return [self.major, sorted(list(self.req)), sorted(list(self.elect))]

    def remaining_req(self, courses):
        """Return the remaining "Required" courses"""
        rem_req = self.req.difference(courses)
        if len(rem_req) == 0:
            return None
        else:
            return rem_req

    def remaining_elect(self, courses):
        """Return remaining elective courses"""
        rem_elect = self.elect.difference(courses)
        if len(rem_elect) < len(self.elect):
            return None
        else:
            return rem_elect

    def completed_courses(self, courses):
        """Return completed, remaining required and remaining elective courses"""
        comp_courses = set()
        valid_grades = ("A", "A-", "B+", "B", "B-", "C+", "C")
        for course, grade in courses.items():
            if grade is None:
                continue
            elif grade in valid_grades:
                comp_courses.add(course)

        rem_req = self.remaining_req(comp_courses)
        rem_elect = self.remaining_elect(comp_courses)

        return sorted(list(comp_courses)), rem_req, rem_elect


class Instructor:
    """Class to store details of instructors"""

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
        self.majors_filepath = os.path.join(dir_path, "majors.txt")

        self.all_students = {}
        self.all_instructors = {}
        self.all_majors = {}

        self.read_files()  # call all read functions
        self.print_pt()  # call to print summary of students and instructors

    def read_files(self):
        """Function call To read files """
        self.read_students()
        self.read_instructors()
        self.read_grades()
        self.read_majors()

    def print_pt(self):
        """Function call to print summary"""
        self.major_prettytable()
        self.student_prettytable()
        self.instructor_prettytable()

    def file_reading_gen(self, filepath, sep, fields, header=True):
        """generator function to read tab separated text files and yield a list with all of the values
        from a single line in the file on each call to next()"""

        try:
            fp = open(filepath)
        except FileNotFoundError:
            print("Error: Cannot Open File at", filepath)
        else:
            with fp:
                line_numb = 0
                for line in fp:
                    line_fields = tuple(line.rstrip('\n').split(sep))
                    line_numb += 1
                    if len(line_fields) != fields:
                        raise ValueError(f"{filepath} has {len(line_fields)} fields on line {line_numb} but expected "
                                         f"{fields}")
                    if header:
                        header = False
                        continue
                    else:
                        yield line.rstrip("\n").split(sep)

    def read_students(self):
        """Read students.txt and store the (Key:CWID) and (Value:instance of Student class) in the dictionary"""
        for student in self.file_reading_gen(self.students_filepath, ";", 3):
            cwid, name, major = student
            if cwid not in self.all_students:
                self.all_students[cwid] = Student(cwid, name, major)

    def read_instructors(self):
        """Read instructors.txt and store the (Key:CWID) and (Value:instance of Instructor class) in the dictionary"""
        for instructor in self.file_reading_gen(self.instructors_filepath, "|", 3):
            cwid, name, dept = instructor
            if cwid not in self.all_instructors:
                self.all_instructors[cwid] = Instructor(cwid, name, dept)

    def read_grades(self):
        """Read grades.txt and update the grade of the course for given student and
        update the count of students enrolled in the course taught by the particular instructor """
        for grade_info in self.file_reading_gen(self.grades_filepath, "|", 4):
            stud_cwid, course, grade, inst_cwid = grade_info
            if stud_cwid in self.all_students.keys():
                self.all_students[stud_cwid].add_course(course, grade)
            else:
                raise ValueError(f"CWID: {stud_cwid} of student not present in students database ")

            if inst_cwid in self.all_instructors.keys():
                self.all_instructors[inst_cwid].add_course(course)
            else:
                raise ValueError(f"CWID: {inst_cwid} of instructor not present in instructors database ")

    def read_majors(self):
        """Read majors.txt and store the courses accordingly"""
        for major, course_type, course in self.file_reading_gen(self.majors_filepath, "\t", 3):
            if major not in self.all_majors:
                self.all_majors[major] = Major(major)

            self.all_majors[major].add_major(course_type, course)

    def major_prettytable(self):
        """Print summary of Majors"""
        pt = PrettyTable(field_names=["Dept", "Required", "Electives"])
        for major in self.all_majors.values():
            dept, req_courses, elec_courses = major.get_major_info()
            pt.add_row([dept, req_courses, elec_courses])

        print("\nMajors Summary")
        print(pt)

    def student_prettytable(self):
        """Print summary of students"""
        pt = PrettyTable(field_names=["CWID", "Name", "Major" ,"Completed Courses", "Remaining Required", "Remaining Electives"])
        for student in self.all_students.values():
            cwid, name, major, courses = student.get_student_info()
            comp, req, elect = self.all_majors[major.major].completed_courses(courses)
            pt.add_row([cwid, name, major.major, comp, req, elect])


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
    path = "C:\\Users\shiva\Desktop\HW10"
    try:
        repo_stevens = Repository(path)
        stud = repo_stevens.all_students.get("10115")
        print("info : ", stud.get_student_info)

    except ValueError:
        print("Error", ValueError)
    except Exception:
        print("Exception", Exception)


if __name__ == "__main__":
    main()