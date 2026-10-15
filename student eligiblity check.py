from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Student:
    name: str
    level: str  
    income: float
    credits: int
    sat: Optional[int]
    major: str
    is_first_gen: bool
    is_veteran: bool
    has_research: bool

@dataclass
class Program:
    id: str
    name: str
    level: str  
    major: str  
    min_gpa: Optional[float]
    max_income: Optional[float]
    min_credits: Optional[int]
    min_sat: Optional[int]
    req_first_gen: bool
    req_veteran: bool
    program_type: str
    amount: str

class EligibilityChecker:
    def __init__(self):
        self.programs: List[Program] = []

    def add_program(self, program: Program):
        self.programs.append(program)

    def evaluate(self, student: Student):
        results = []
        
        for prog in self.programs:
            is_eligible = True
            reasons = []

            # Level check
            if prog.level != "Any" and prog.level != student.level:
                is_eligible = False
                reasons.append(f"Requires {prog.level} status (you are {student.level})")

            # GPA check
            if prog.min_gpa is not None and student.gpa < prog.min_gpa:
                is_eligible = False
                reasons.append(f"Minimum GPA required: {prog.min_gpa} (your GPA: {student.gpa})")

            # Income check
            if prog.max_income is not None and student.income > prog.max_income:
                is_eligible = False
                reasons.append(f"Maximum family income: ${prog.max_income:,.2f} (your income: ${student.income:,.2f})")

            # Credits check
            if prog.min_credits is not None and student.credits < prog.min_credits:
                is_eligible = False
                reasons.append(f"Minimum credits required: {prog.min_credits} (you have {student.credits})")

            # SAT check
            if prog.min_sat is not None:
                if student.sat is None or student.sat < prog.min_sat:
                    is_eligible = False
                    sat_display = student.sat if student.sat is not None else "Not Provided"
                    reasons.append(f"Minimum SAT required: {prog.min_sat} (your SAT: {sat_display})")

            # Major check
            if prog.major != "Any" and prog.major != student.major and student.major != "Any":
                is_eligible = False
                reasons.append(f"Restricted to major: {prog.major} (your major: {student.major})")

            # First Gen check
            if prog.req_first_gen and not student.is_first_gen:
                is_eligible = False
                reasons.append("Must be a first-generation student")

            # Veteran check
            if prog.req_veteran and not student.is_veteran:
                is_eligible = False
                reasons.append("Must be a military veteran or dependent")

            results.append({
                "program": prog,
                "is_eligible": is_eligible,
                "reasons": reasons
            })
            
        return results

    def print_report(self, student: Student):
        print("="*50)
        print(f"ELIGIBILITY REPORT FOR: {student.name.upper()}")
        print("="*50)
        
        evaluations = self.evaluate(student)
        eligible = [res for res in evaluations if res["is_eligible"]]
        ineligible = [res for res in evaluations if not res["is_eligible"]]
        
        print(f"\n✅ MATCHED PROGRAMS ({len(eligible)} found):")
        if not eligible:
            print("   (None matched current criteria)")
        for res in eligible:
            p = res["program"]
            print(f"   - {p.name} ({p.program_type}: {p.amount})")

        print(f"\n❌ UNMET PROGRAMS ({len(ineligible)} found):")
        for res in ineligible:
            p = res["program"]
            print(f"   - {p.name}")
            for r in res["reasons"]:
                print(f"       * {r}")
        print("\n")

if __name__ == "__main__":
    checker = EligibilityChecker()

    # 1. Load System Database
    checker.add_program(Program("p1", "Presidential Honors Scholarship", "Undergraduate", "Any", 3.8, None, 12, 1400, False, False, "Scholarship", "$15,000 / yr"))
    checker.add_program(Program("p2", "STEM Innovation Grant", "Undergraduate", "STEM", 3.4, 75000, 30, None, False, False, "Grant", "$8,500"))
    checker.add_program(Program("p3", "First-Gen Opportunity Fund", "Any", "Any", 2.8, 60000, 0, None, True, False, "Financial Aid", "$5,000"))
    checker.add_program(Program("p4", "Military Veteran Education Support", "Any", "Any", 2.5, None, 0, None, False, True, "Special Aid", "Full Tuition"))
    checker.add_program(Program("p5", "Computer Science Elite Program", "Undergraduate", "Computer Science", 3.6, None, 45, 1300, False, False, "Honors Program", "$10,000"))

    # 2. Test Case A: High Achiever Student
    student_a = Student(
        name="Samantha Wright",
        level="Undergraduate",
        gpa=3.92,
        income=85000,
        credits=60,
        sat=1480,
        major="Computer Science",
        is_first_gen=False,
        is_veteran=False,
        has_research=True
    )

    # 3. Test Case B: Financial Need / First-Gen Student
    student_b = Student(
        name="Marcus Vance",
        level="Undergraduate",
        gpa=3.25,
        income=32000,
        credits=15,
        sat=None,
        major="Business & Economics",
        is_first_gen=True,
        is_veteran=True,
        has_research=False
    )
    checker.print_report(student_a)
    checker.print_report(student_b)