# Role Permissions Matrix

This document defines platform roles, cohort roles, permissions, and role management workflows.

## Platform Roles

### Student
**Permissions:**
- View curriculum content
- Complete lessons and assessments
- Track personal progress
- View own grades and feedback
- Participate in discussion forums
- Use AI learning assistant
- View own notifications

**Restrictions:**
- Cannot modify curriculum content
- Cannot access admin features
- Cannot change own grades
- Cannot view other students' personal information

### Instructor
**Permissions:**
- All student permissions, plus:
- View assigned students' progress
- Grade assessments (short answer questions)
- Provide feedback and comments
- View class analytics and trends
- Create cohorts and manage enrollment
- Set assignment deadlines
- Moderate discussions
- Create announcements
- Export student reports
- Access grading queue

**Restrictions:**
- Cannot modify core curriculum (unless also admin)
- Cannot access other instructors' cohorts (unless shared)
- Cannot change system settings

### Admin
**Permissions:**
- All instructor permissions, plus:
- Modify curriculum content
- Create/edit modules and assessments
- Assign instructors to cohorts
- View platform-wide analytics
- Manage user accounts
- Configure system settings
- Export all data
- Promote users to instructor/admin roles

**Restrictions:**
- None (full system access)

## Cohort Roles

### Student (within cohort)
**Permissions:**
- View cohort-specific content
- Participate in cohort discussions
- View cohort leaderboard (if opt-in)
- See cohort deadlines

### Instructor (within cohort)
**Permissions:**
- All cohort student permissions, plus:
- Enroll/remove students from cohort
- Create cohort deadlines
- Create cohort announcements
- View cohort analytics
- Grade assessments for cohort students
- Moderate cohort discussions

## Permission Inheritance

- **Admin** can perform all instructor actions
- **Instructor** can perform all student actions
- **Platform role** applies globally across all cohorts
- **Cohort role** applies only within specific cohort context

## Role Promotion Workflow

### Initial Admin Creation
- First admin created via database seed script or manual database insert
- Admin account should be created during initial setup

### Creating Instructors
- Admin can promote users to instructor role via admin interface or endpoint
- Or instructors can be created via seed script for testing

### Role Changes
- Role changes should be audited (track who changed role, when, why)
- Role demotion (admin → instructor → student) requires admin approval
- Users cannot change their own role

## Edge Cases

### Can Admin Be Student in a Cohort?
- Yes, admin can be enrolled as student in cohort
- Platform role (admin) is separate from cohort role (student)
- Admin retains admin permissions while in cohort

### Can Instructor Be Student in Another Cohort?
- Yes, instructor can be student in different cohort
- Platform role (instructor) allows them to also be student elsewhere
- Each cohort maintains separate role context

### Multiple Cohort Roles
- User can have different roles in different cohorts
- Example: Instructor in Cohort A, Student in Cohort B
- Cohort roles are stored in `cohort_members` table

## Authorization Rules

### Platform-Level Authorization
- Check `users.role` for platform-wide permissions
- Student, Instructor, Admin roles apply globally

### Cohort-Level Authorization
- Check `cohort_members.role` for cohort-specific permissions
- Student, Instructor roles apply within cohort context
- Platform admin can access all cohorts regardless of membership

## Implementation Notes

- JWT tokens should include both platform role and cohort memberships
- API endpoints should check appropriate role level (platform vs cohort)
- UI should conditionally render based on user's roles
- Backend should enforce role checks for all sensitive operations

---

**Last Updated:** 2025-02-15

