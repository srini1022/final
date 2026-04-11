"""
AI Validation Agent - Example Implementation
Validates student data and makes auto-approval decisions
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Tuple
from enum import Enum


class ValidationSeverity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class ValidationStatus(Enum):
    AUTO_APPROVED = "auto_approved"
    TRANSFERRED = "transferred"
    REJECTED = "rejected"


class ValidationRule:
    """Represents a single validation rule"""
    
    def __init__(self, name: str, rule_type: str, check_func, score: int, severity: str):
        self.name = name
        self.rule_type = rule_type
        self.check_func = check_func
        self.score = score
        self.severity = severity
    
    def validate(self, data: Dict) -> Tuple[bool, str]:
        """Execute validation and return (passed, message)"""
        try:
            result = self.check_func(data)
            return result
        except Exception as e:
            return False, f"Error in {self.name}: {str(e)}"


class ValidationAgent:
    """AI Agent for validating student requests"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
        self.validation_results = []
        self.decision_log = []
    
    def _initialize_rules(self) -> List[ValidationRule]:
        """Initialize all validation rules"""
        rules = []
        
        # ===== LAYER 1: COMPLETENESS CHECKS =====
        
        # Required fields
        rules.append(ValidationRule(
            name="Required Fields Present",
            rule_type="required_field",
            check_func=self._check_required_fields,
            score=10,
            severity=ValidationSeverity.CRITICAL.value
        ))
        
        # Email format
        rules.append(ValidationRule(
            name="Email Format Valid",
            rule_type="format",
            check_func=self._check_email_format,
            score=5,
            severity=ValidationSeverity.WARNING.value
        ))
        
        # Phone format
        rules.append(ValidationRule(
            name="Phone Format Valid",
            rule_type="format",
            check_func=self._check_phone_format,
            score=5,
            severity=ValidationSeverity.WARNING.value
        ))
        
        # USN format
        rules.append(ValidationRule(
            name="USN Format Valid",
            rule_type="format",
            check_func=self._check_usn_format,
            score=5,
            severity=ValidationSeverity.WARNING.value
        ))
        
        # No suspicious patterns
        rules.append(ValidationRule(
            name="No Suspicious Patterns",
            rule_type="format",
            check_func=self._check_suspicious_patterns,
            score=5,
            severity=ValidationSeverity.INFO.value
        ))
        
        # ===== LAYER 2: DATABASE VERIFICATION =====
        
        # USN exists in database
        rules.append(ValidationRule(
            name="USN Found in Database",
            rule_type="database_check",
            check_func=self._check_usn_in_database,
            score=15,
            severity=ValidationSeverity.CRITICAL.value
        ))
        
        # Name matches database
        rules.append(ValidationRule(
            name="Name Matches Database",
            rule_type="database_check",
            check_func=self._check_name_matches,
            score=10,
            severity=ValidationSeverity.WARNING.value
        ))
        
        # Enrollment status active
        rules.append(ValidationRule(
            name="Enrollment Status Active",
            rule_type="database_check",
            check_func=self._check_enrollment_status,
            score=10,
            severity=ValidationSeverity.CRITICAL.value
        ))
        
        # Fees paid
        rules.append(ValidationRule(
            name="Fees Paid",
            rule_type="database_check",
            check_func=self._check_fees_paid,
            score=5,
            severity=ValidationSeverity.WARNING.value
        ))
        
        # ===== LAYER 3: CONSISTENCY CHECKS =====
        
        # No discrepancies
        rules.append(ValidationRule(
            name="No Data Discrepancies",
            rule_type="consistency",
            check_func=self._check_no_discrepancies,
            score=20,
            severity=ValidationSeverity.WARNING.value
        ))
        
        # Department matches
        rules.append(ValidationRule(
            name="Department Matches Database",
            rule_type="consistency",
            check_func=self._check_department_matches,
            score=10,
            severity=ValidationSeverity.INFO.value
        ))
        
        return rules
    
    # ===== VALIDATION CHECK FUNCTIONS =====
    
    def _check_required_fields(self, data: Dict) -> Tuple[bool, str]:
        """Check if all required fields are present"""
        required = ['name', 'usn', 'email', 'phone', 'department', 'request_type']
        missing = [f for f in required if not data.get(f)]
        
        if missing:
            return False, f"Missing fields: {', '.join(missing)}"
        return True, "All required fields present"
    
    def _check_email_format(self, data: Dict) -> Tuple[bool, str]:
        """Validate email format"""
        email = data.get('email', '')
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, f"Invalid email format: {email}"
        return True, "Email format valid"
    
    def _check_phone_format(self, data: Dict) -> Tuple[bool, str]:
        """Validate phone format"""
        phone = data.get('phone', '')
        pattern = r'^\d{10}$'
        
        if not re.match(pattern, phone):
            return False, f"Invalid phone format: {phone} (must be 10 digits)"
        return True, "Phone format valid"
    
    def _check_usn_format(self, data: Dict) -> Tuple[bool, str]:
        """Validate USN format"""
        usn = data.get('usn', '')
        pattern = r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$'
        
        if not re.match(pattern, usn):
            return False, f"Invalid USN format: {usn}"
        return True, "USN format valid"
    
    def _check_suspicious_patterns(self, data: Dict) -> Tuple[bool, str]:
        """Check for suspicious patterns"""
        suspicious_keywords = ['test', 'fake', 'dummy', 'admin', 'root']
        
        for field in ['name', 'email']:
            value = str(data.get(field, '')).lower()
            if any(keyword in value for keyword in suspicious_keywords):
                return False, f"Suspicious pattern detected in {field}"
        
        return True, "No suspicious patterns"
    
    def _check_usn_in_database(self, data: Dict) -> Tuple[bool, str]:
        """Check if USN exists in college database"""
        # In real implementation, query actual database
        # For demo, we'll simulate with a mock database
        mock_db = {
            'CS22CS001': {'name': 'John Doe', 'department': 'CSE', 'status': 'active', 'fees': 'paid'},
            'CS22CS002': {'name': 'Jane Smith', 'department': 'CSE', 'status': 'active', 'fees': 'paid'},
            'CS22CS003': {'name': 'Bob Johnson', 'department': 'CSE', 'status': 'inactive', 'fees': 'pending'},
        }
        
        usn = data.get('usn', '')
        if usn not in mock_db:
            return False, f"USN {usn} not found in database"
        
        # Store database record for later use
        data['_db_record'] = mock_db[usn]
        return True, f"USN {usn} found in database"
    
    def _check_name_matches(self, data: Dict) -> Tuple[bool, str]:
        """Check if name matches database"""
        db_record = data.get('_db_record')
        if not db_record:
            return False, "Database record not found"
        
        submitted_name = data.get('name', '').lower().strip()
        db_name = db_record.get('name', '').lower().strip()
        
        # Fuzzy match (allow minor differences)
        if submitted_name == db_name:
            return True, "Name matches database exactly"
        elif self._fuzzy_match(submitted_name, db_name):
            return True, "Name matches database (minor differences)"
        else:
            return False, f"Name mismatch: submitted '{data.get('name')}' vs database '{db_record.get('name')}'"
    
    def _check_enrollment_status(self, data: Dict) -> Tuple[bool, str]:
        """Check if student enrollment is active"""
        db_record = data.get('_db_record')
        if not db_record:
            return False, "Database record not found"
        
        status = db_record.get('status', '').lower()
        if status == 'active':
            return True, "Enrollment status is active"
        else:
            return False, f"Enrollment status is {status}, not active"
    
    def _check_fees_paid(self, data: Dict) -> Tuple[bool, str]:
        """Check if fees are paid"""
        db_record = data.get('_db_record')
        if not db_record:
            return False, "Database record not found"
        
        fees = db_record.get('fees', '').lower()
        if fees == 'paid':
            return True, "Fees are paid"
        else:
            return False, f"Fees status is {fees}, not paid"
    
    def _check_no_discrepancies(self, data: Dict) -> Tuple[bool, str]:
        """Check for data discrepancies"""
        db_record = data.get('_db_record')
        if not db_record:
            return False, "Database record not found"
        
        discrepancies = []
        
        # Check department
        if data.get('department', '').upper() != db_record.get('department', '').upper():
            discrepancies.append(f"Department mismatch")
        
        if discrepancies:
            return False, f"Discrepancies found: {', '.join(discrepancies)}"
        return True, "No discrepancies found"
    
    def _check_department_matches(self, data: Dict) -> Tuple[bool, str]:
        """Check if department matches database"""
        db_record = data.get('_db_record')
        if not db_record:
            return False, "Database record not found"
        
        submitted_dept = data.get('department', '').upper()
        db_dept = db_record.get('department', '').upper()
        
        if submitted_dept == db_dept:
            return True, "Department matches database"
        else:
            return False, f"Department mismatch: {submitted_dept} vs {db_dept}"
    
    def _fuzzy_match(self, str1: str, str2: str, threshold: float = 0.8) -> bool:
        """Simple fuzzy string matching"""
        # Calculate similarity (simplified Levenshtein-like approach)
        if len(str1) == 0 or len(str2) == 0:
            return str1 == str2
        
        matches = sum(1 for a, b in zip(str1, str2) if a == b)
        similarity = matches / max(len(str1), len(str2))
        return similarity >= threshold
    
    # ===== VALIDATION PIPELINE =====
    
    def validate_request(self, request_data: Dict) -> Dict:
        """
        Main validation pipeline
        Returns validation results and decision
        """
        print(f"\n{'='*60}")
        print(f"VALIDATING REQUEST FOR: {request_data.get('name')}")
        print(f"{'='*60}\n")
        
        # Run all validation rules
        validation_results = []
        total_score = 0
        issues = {'critical': [], 'warning': [], 'info': []}
        
        for rule in self.rules:
            passed, message = rule.validate(request_data)
            
            result = {
                'rule': rule.name,
                'type': rule.rule_type,
                'passed': passed,
                'message': message,
                'score': rule.score if passed else 0,
                'severity': rule.severity
            }
            
            validation_results.append(result)
            
            if passed:
                total_score += rule.score
                print(f"✅ {rule.name}: {message} (+{rule.score} pts)")
            else:
                print(f"❌ {rule.name}: {message}")
                issues[rule.severity].append(message)
        
        # Make decision based on score and issues
        decision = self._make_decision(total_score, issues)
        
        # Prepare response
        response = {
            'request_id': request_data.get('request_id'),
            'student_name': request_data.get('name'),
            'validation_score': total_score,
            'validation_status': decision['status'],
            'decision': decision['action'],
            'destination': decision['destination'],
            'reason': decision['reason'],
            'issues': issues,
            'validation_details': validation_results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Log decision
        self._log_decision(response)
        
        return response
    
    def _make_decision(self, score: int, issues: Dict) -> Dict:
        """
        Decision engine
        Determines if request should be auto-approved or transferred
        """
        print(f"\n{'─'*60}")
        print(f"DECISION ENGINE")
        print(f"{'─'*60}")
        print(f"Total Score: {score}/100")
        print(f"Critical Issues: {len(issues['critical'])}")
        print(f"Warnings: {len(issues['warning'])}")
        print(f"Info: {len(issues['info'])}\n")
        
        # Decision logic
        if score >= 85 and not issues['critical']:
            decision = {
                'status': ValidationStatus.AUTO_APPROVED.value,
                'action': 'AUTO_APPROVE',
                'destination': 'HOD',
                'reason': 'All data verified and complete. Student enrollment confirmed, fees paid, no critical issues found.'
            }
            print("🎯 DECISION: AUTO-APPROVE")
            print("📤 DESTINATION: Send directly to HOD (skip manager)")
        
        elif score >= 70 and issues['warning'] and not issues['critical']:
            decision = {
                'status': ValidationStatus.TRANSFERRED.value,
                'action': 'TRANSFER',
                'destination': 'MANAGER',
                'reason': f'Minor issues found that need review: {"; ".join(issues["warning"])}'
            }
            print("⚠️  DECISION: TRANSFER TO MANAGER")
            print("📤 DESTINATION: Manager review required")
        
        else:
            decision = {
                'status': ValidationStatus.TRANSFERRED.value,
                'action': 'TRANSFER',
                'destination': 'MANAGER',
                'reason': f'Critical issues found: {"; ".join(issues["critical"] + issues["warning"])}'
            }
            print("🚨 DECISION: TRANSFER TO MANAGER")
            print("📤 DESTINATION: Manager review required (critical issues)")
        
        print(f"📝 Reason: {decision['reason']}\n")
        return decision
    
    def _log_decision(self, response: Dict):
        """Log decision for audit trail"""
        self.decision_log.append(response)
    
    def get_decision_log(self) -> List[Dict]:
        """Get all decisions made by agent"""
        return self.decision_log


# ===== EXAMPLE USAGE =====

if __name__ == "__main__":
    # Initialize agent
    agent = ValidationAgent()
    
    # Test Case 1: Perfect Request (should auto-approve)
    print("\n" + "="*60)
    print("TEST CASE 1: PERFECT REQUEST")
    print("="*60)
    
    perfect_request = {
        'request_id': 1,
        'name': 'John Doe',
        'usn': 'CS22CS001',
        'email': 'john@college.edu',
        'phone': '9876543210',
        'department': 'CSE',
        'request_type': 'Certificate',
        'reason': 'Internship application'
    }
    
    result1 = agent.validate_request(perfect_request)
    print(f"\n✅ RESULT: {result1['decision']}")
    print(f"📊 Score: {result1['validation_score']}/100")
    print(f"📤 Destination: {result1['destination']}")
    
    # Test Case 2: Request with warnings (should transfer to manager)
    print("\n" + "="*60)
    print("TEST CASE 2: REQUEST WITH WARNINGS")
    print("="*60)
    
    warning_request = {
        'request_id': 2,
        'name': 'Jane Smith',
        'usn': 'CS22CS002',
        'email': 'jane@college.edu',
        'phone': '9876543210',
        'department': 'IT',  # Different from database (CSE)
        'request_type': 'Certificate',
        'reason': 'Internship application'
    }
    
    result2 = agent.validate_request(warning_request)
    print(f"\n⚠️  RESULT: {result2['decision']}")
    print(f"📊 Score: {result2['validation_score']}/100")
    print(f"📤 Destination: {result2['destination']}")
    
    # Test Case 3: Request with critical issues (should transfer to manager)
    print("\n" + "="*60)
    print("TEST CASE 3: REQUEST WITH CRITICAL ISSUES")
    print("="*60)
    
    critical_request = {
        'request_id': 3,
        'name': 'Unknown Student',
        'usn': 'CS22CS999',  # Not in database
        'email': 'invalid-email',  # Invalid format
        'phone': '123',  # Invalid format
        'department': 'CSE',
        'request_type': 'Certificate',
        'reason': 'Internship application'
    }
    
    result3 = agent.validate_request(critical_request)
    print(f"\n🚨 RESULT: {result3['decision']}")
    print(f"📊 Score: {result3['validation_score']}/100")
    print(f"📤 Destination: {result3['destination']}")
    
    # Print decision log
    print("\n" + "="*60)
    print("AGENT DECISION LOG")
    print("="*60)
    
    for i, decision in enumerate(agent.get_decision_log(), 1):
        print(f"\nDecision #{i}:")
        print(f"  Student: {decision['student_name']}")
        print(f"  Score: {decision['validation_score']}/100")
        print(f"  Status: {decision['validation_status']}")
        print(f"  Destination: {decision['destination']}")
        print(f"  Reason: {decision['reason']}")
