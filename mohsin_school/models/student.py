from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean('Is Student')
    is_parent_student = fields.Boolean('Is Parent Student', store=True, compute='_compute_parent')
    contact_type = fields.Selection([
        ('parent', 'Parent'),
        ('address', 'Address'),
    ], string='Contact Type', default='parent')
    relation = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
        ('grand-father', 'Grand Father'),
        ('grand-mother', 'Grand Mother'),
        ('other', 'Other'),
    ], string='Relation')
    is_guardian = fields.Boolean('Is Guardian')
    roll_no = fields.Char('Roll No')
    admission_no = fields.Char('Admission No')
    guardian_name = fields.Char("Guardian Name")





    course_id = fields.Many2one('mohsin.school.course', string='Course')
    use_batch = fields.Boolean(related='course_id.use_batch_subject')
    batch_id = fields.Many2one('mohsin.school.course.batch', string='Batch',
                               domain="[('course_id','=',course_id)]"
                               )
    use_section = fields.Boolean(related='course_id.use_section')
    section_id = fields.Many2one('mohsin.school.course.section', string='Section',
                                 domain="[('course_id','=',course_id)]"
                                 )
    student_subject_line = fields.One2many('res.partner.subjects.line', 'student_id', 'Subjects')
    enrollment_count = fields.Integer(string='Enrollments', compute='_compute_enrollment_count')

    med_info_ids = fields.One2many('mohsin.school.student.medical', 'student_id', 'Medical Info')
    med_info_count = fields.Integer(string='Enrollments', compute='_compute_med_info_count')

    sibling_ids = fields.One2many('mohsin.student.sibling', 'partner_id', 'Siblings')

    date_birth = fields.Date(string='Date of Birth')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')

    merital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('divorced', 'Divorced'),
        ('other', 'Other'),
    ], string='Merital Status')

    country_birth = fields.Many2one('res.country', 'Country of Birth')
    country_nationality = fields.Many2one('res.country', 'Nationality')

    guardian_id = fields.Many2one('res.partner', string='Gaurdian', readonly=True, store=True,
                                  help='A guardian is a person responsible for the student.',
                                  )

    student_complexion = fields.Char('Complexion')
    student_weight = fields.Float('Weight (in kg)')
    student_height = fields.Float('Height (in cm)')
    student_mark_identify = fields.Text('Mark for Identity')
    student_emergency_contact = fields.Char('Emergency Contact Name')
    student_emergency_phone = fields.Char('Emergency Contact Number')
    # codee = fields.Char(string="course code")

    # @api.depends('course_id')
    # def _compute_roll_no(self):
    #     c = 'schoolcourse.' + str(self.course_id.code)
    #     self.roll_no = str(self.env['ir.sequence'].next_by_code(c))



    # @api.model
    # def create(self, vals):
    #     if vals['is_student'] == True:
    #         c = self.env['mohsin.school.course'].browse(vals['course_id'])
    #         sq_number = 'schoolcourse.' + str(c.code)
    #         vals['roll_no'] = str(self.env['ir.sequence'].next_by_code(sq_number))
    #         return super(ResPartner, self).create(vals)



    def _compute_med_info_count(self):
        for record in self:
            record.med_info_count = len(record.med_info_ids)


    def _compute_enrollment_count(self):
        enrollment_ids = self.env['mohsin.school.student.enrollment']
        for record in self:
            record.enrollment_count = len(enrollment_ids.search([('model','=',self._name),('res_id','=',record.id)]))


    @api.depends('parent_id')
    def _compute_parent(self):
        for record in self:
            if record.parent_id.is_student:
                record.is_parent_student = True
            else:
                record.is_parent_student = False


    def generate_roll_number(self):
        students = self.env['res.partner'].browse(self.env.context.get('active_ids'))
        for student in students:
            if not student.roll_no:
                number = student.course_id.sequence_id.next_by_id()
                student.write({
                    'roll_no': number,
                })


    def open_enrollment_history(self):
        enrollment_ids = self.env['mohsin.school.student.enrollment'].search(
            [('model', '=', self._name), ('res_id', '=', self.id)])
        action = self.env.ref('mohsin_school.action_enrollment_history').read()[0]
        action.update({
            'name': 'Enrollment History',
            'view_mode': 'tree',
            'res_model': 'mohsin.school.student.enrollment',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', enrollment_ids.ids)],
            'context': {
                'default_model': self._name,
                'default_res_id': self.id,
            },
        })
        return action


    def open_medical_info(self):
        action = self.env.ref('mohsin_school.action_medical_history').read()[0]
        action.update({
            'name': 'Medical History',
            'view_mode': 'tree',
            'res_model': 'mohsin.school.student.medical',
            'type': 'ir.actions.act_window',
            'domain': [('student_id','=',self.id)],
            'context': {
                'default_student_id': self.id,
            },
        })
        return action




class StudentSiblings(models.Model):
    _name = 'mohsin.student.sibling'
    _description = 'Student Sibling'

    name = fields.Many2one('res.partner', 'Student Name',
                           domain="[('is_student','=',True),('is_parent_student','=',False)]", required=True)
    partner_id = fields.Many2one('res.partner', string='Student', required=True, ondelete='cascade', index=True,
                                 copy=False)
    course_id = fields.Many2one('mohsin.school.course', string='Course')
    roll_no = fields.Char(string='Roll Number')
    date_birth = fields.Date('Date of Birth')
    relation = fields.Selection([
        ('brother', 'Brother'),
        ('sister', 'Sister'),
    ], string='Gender', default='brother', required=True)




class SubjectLine(models.Model):
    _name = 'res.partner.subjects.line'
    _description = 'Student Sibling'

    student_id = fields.Many2one('res.partner',
                                 string='Student',
                                 required=True,
                                 ondelete='cascade',
                                 index=True, copy=False
                                 )
    subject_id = fields.Many2one('mohsin.school.subject', string='Subject',
                                 required=True,
                                 domain="[('id','in',subject_ids)]"
                                 )
    subject_ids = fields.Many2many(
        comodel_name='mohsin.school.subject',
        string='Courses for Subject',
        compute='_compute_subjects_from_course',
    )

    _sql_constraints = [
        ('unique_student_subject', 'UNIQUE(student_id, subject_id)', 'Subject must be unique!'),
    ]

    @api.depends('student_id.course_id')
    def _compute_subjects_from_course(self):
        for record in self:
            if record.student_id.course_id:
                subject_ids = self.env['mohsin.school.course.subject.line'].search([
                    ('course_id', '=', record.student_id.course_id.id)
                ]).mapped('subject_id')
                record.subject_ids = subject_ids
            else:
                record.subject_ids = False