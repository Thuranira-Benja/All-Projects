from django.core.management.base import BaseCommand
from constitution.models import Constitution

class Command(BaseCommand):
    help = 'Add constitution data to the database'

    def handle(self, *args, **options):
        content = """
<h1 style="color: #0A7D3B; margin-bottom: 20px;">PREAMBLE</h1>
<p>We, the members of Meru Young Professionals (MYP), in pursuit of excellence, leadership, and community development, do hereby establish and adopt this Constitution to govern our organization.</p>
<p>Recognizing the need for a structured framework that promotes integrity, accountability, and service, we commit to upholding the principles and values enshrined in this document.</p>
<p>This Constitution shall serve as the guiding document for all activities, decisions, and operations of Meru Young Professionals.</p>

<h1 style="color: #0A7D3B; margin-top: 30px; margin-bottom: 20px;">ARTICLE I: NAME AND ESTABLISHMENT</h1>
<p><strong>Section 1.1:</strong> The organization shall be known as "Meru Young Professionals" (MYP).</p>
<p><strong>Section 1.2:</strong> MYP is a non-political, non-profit youth-led organization established to bring together professionals from the Mt. Kenya region and beyond.</p>
<p><strong>Section 1.3:</strong> The organization shall be registered under the relevant laws and regulations of Kenya.</p>
<p><strong>Section 1.4:</strong> The principal office of MYP shall be located in Meru Town, Kenya.</p>

<h1 style="color: #0A7D3B; margin-top: 30px; margin-bottom: 20px;">ARTICLE II: VISION AND MISSION</h1>
<p><strong>Vision:</strong> To become the leading network of transformative young professionals creating positive impact across Kenya and beyond.</p>
<p><strong>Mission:</strong> To empower young professionals through leadership development, innovation, entrepreneurship, mentorship, community service, and sustainable growth.</p>

<h3 style="color: #0A7D3B; margin-top: 20px;">Objectives</h3>
<ul>
    <li>To create a platform for professional networking and collaboration</li>
    <li>To provide mentorship and career development opportunities</li>
    <li>To implement community-based projects that create measurable impact</li>
    <li>To promote entrepreneurship and innovation among youth</li>
    <li>To advocate for youth participation in leadership and governance</li>
</ul>

<h1 style="color: #0A7D3B; margin-top: 30px; margin-bottom: 20px;">ARTICLE III: CORE VALUES</h1>
<p>MYP is guided by the following core values:</p>
<ul>
    <li><strong>Integrity:</strong> Acting with honesty and transparency in all dealings.</li>
    <li><strong>Accountability:</strong> Taking responsibility for our actions and commitments.</li>
    <li><strong>Excellence:</strong> Striving for the highest standards in everything we do.</li>
    <li><strong>Innovation:</strong> Embracing new ideas and creative solutions.</li>
    <li><strong>Teamwork:</strong> Working together to achieve greater impact.</li>
    <li><strong>Professionalism:</strong> Maintaining high professional standards.</li>
    <li><strong>Service:</strong> Dedicating ourselves to community service.</li>
    <li><strong>Inclusivity:</strong> Welcoming all professionals regardless of background.</li>
</ul>

<h1 style="color: #0A7D3B; margin-top: 30px; margin-bottom: 20px;">ARTICLE IV: MEMBERSHIP</h1>
<p><strong>Section 4.1: Eligibility</strong><br>Membership is open to young professionals aged 18-35 years from the Mt. Kenya region and beyond who align with MYP's vision and values.</p>
<p><strong>Section 4.2: Registration</strong><br>Members shall register through the official MYP platform and pay the prescribed membership fees as determined by the Executive Council.</p>
<p><strong>Section 4.3: Rights of Members</strong><br>Members shall enjoy the following rights:</p>
<ul>
    <li>Voting in general elections and referendums</li>
    <li>Accessing mentorship and training programs</li>
    <li>Participating in events and projects</li>
    <li>Standing for leadership positions</li>
    <li>Accessing member benefits and resources</li>
</ul>
<p><strong>Section 4.4: Obligations of Members</strong><br>Members are expected to:</p>
<ul>
    <li>Uphold the values and Constitution of MYP</li>
    <li>Pay membership fees promptly</li>
    <li>Participate actively in activities</li>
    <li>Contribute positively to the organization's goals</li>
    <li>Respect other members and leaders</li>
</ul>

<h1 style="color: #0A7D3B; margin-top: 30px; margin-bottom: 20px;">ARTICLE V: LEADERSHIP STRUCTURE</h1>
<p><strong>Section 5.1: Executive Council</strong><br>The Executive Council shall be the highest leadership body comprising:</p>
<ul>
    <li>Chairperson</li>
    <li>Vice Chairperson</li>
    <li>Secretary General</li>
    <li>Treasurer</li>
    <li>Program Coordinators (as needed)</li>
</ul>
<p><strong>Section 5.2: Terms of Office</strong><br>Leaders shall serve a term of two years and may be re-elected for a maximum of two consecutive terms.</p>

<h1 style="color: #0A7D3B; margin-top: 30px; margin-bottom: 20px;">ARTICLE VI: GOVERNANCE</h1>
<p><strong>Section 6.1: Executive Council Meetings</strong><br>The Executive Council shall meet monthly to review progress, make strategic decisions, and address emerging issues.</p>
<p><strong>Section 6.2: General Assemblies</strong><br>Annual General Meetings shall be held every December to present annual reports, review financial statements, and elect new leaders.</p>

<h1 style="color: #0A7D3B; margin-top: 30px; margin-bottom: 20px;">ARTICLE VII: AMENDMENTS</h1>
<p><strong>Section 7.1:</strong> This constitution may be amended by a two-thirds majority vote of the Executive Council.</p>
<p><strong>Section 7.2:</strong> Amendments shall take effect immediately upon approval and documentation in the official records.</p>

<h1 style="color: #0A7D3B; margin-top: 30px; margin-bottom: 20px;">ADOPTION</h1>
<p>This Constitution was adopted on January 1, 2024, by the founding members of Meru Young Professionals.</p>

<div style="margin-top: 40px; display: flex; justify-content: space-between; max-width: 500px;">
    <div>
        <p>_____________________</p>
        <p><strong>John Mwangi</strong></p>
        <p>Chairperson</p>
    </div>
    <div>
        <p>_____________________</p>
        <p><strong>Jane Wanjiku</strong></p>
        <p>Secretary General</p>
    </div>
</div>
"""

        constitution, created = Constitution.objects.get_or_create(
            title="MYP Constitution",
            defaults={
                'version': '1.0',
                'content': content,
                'effective_date': '2024-01-01',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Constitution created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Constitution already exists. Updating content...'))
            constitution.content = content
            constitution.save()
            self.stdout.write(self.style.SUCCESS('✅ Constitution updated successfully!'))
