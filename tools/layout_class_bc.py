#!/usr/bin/env python3
"""Ve tay class_b + class_c: grid 3x2 / 2x2, routing lanh rieng, khong de nhau.
Du lieu khop schema.prisma + service methods (da doi chieu).
Dat trong tools/ theo ky luat Dedicated Tools Directory.
"""
import sys
sys.path.insert(0, "E:/HOC TAP/my-project/sp-agent/tools")
from draw_diagram import Diagram

# ================= Hinh 3.7: ket noi & hoi thoai (3 cot x 2 hang) =================
d = Diagram(1700, 660)
X = [120, 640, 1160]
W = 440
Y1, Y2 = 70, 420
B = {}
B["U"] = d.box("U", X[0], Y1, W, "C", "User",
               [["+id: String", "+email: String", "+role: Role"]])
B["C"] = d.box("C", X[1], Y1, W, "C", "ConnectionRequest",
               [["+id: String", "+message: String", "+status: ConnectionStatus"],
                ["+sendRequest(): ConnectionRequest", "+accept(): Conversation",
                 "+reject(): void", "+cancel(): void"]])
B["V"] = d.box("V", X[2], Y1, W, "C", "Conversation",
               [["+id: String", "+lastMessageAt: DateTime"],
                ["+getUserConversations(): Conversation[]", "+getMessages(): Message[]"]])
B["T"] = d.box("T", X[0], Y2, W, "C", "TutorProfile",
               [["+id: String", "+headline: String", "+verificationStatus: VerificationStatus"]])
B["M"] = d.box("M", X[1], Y2, W, "C", "Message",
               [["+id: String", "+content: String"], ["+sendMessage(): Message"]])
B["VP"] = d.box("VP", X[2], Y2, W, "C", "ConversationParticipant",
                [["+id: String", "+hasUnread: Boolean"]])

d.edge([(560, 140), (600, 140), (600, 195), (640, 195)], label="sends", m_start="1", m_end="0..*")
d.edge([(1080, 195), (1120, 195), (1120, 170), (1160, 170)], label="opens", m_start="1", m_end="0..1")
d.edge([(340, 420), (340, 345), (840, 345), (840, 320)], label="receives", m_start="1", m_end="0..*")
d.edge([(1380, 242), (1380, 395), (950, 395), (950, 420)], label="contains", m_start="1", m_end="0..*")
d.edge([(1300, 242), (1300, 420)], label="includes", m_start="1", m_end="2..*")
d.edge([(1300, 536), (1300, 600), (60, 600), (60, 140), (120, 140)], label="is", m_start="*", m_end="1")
d.edge([(450, 212), (450, 370), (780, 370), (780, 420)], label="sends", m_start="1", m_end="0..*")
d.save("E:/HOC TAP/my-project/ecosystem_ketnoi_giasu/docs/diagrams/class_b_connection")

# ================= Hinh 3.8: danh gia & bao cao (2 cot x 2 hang) =================
e = Diagram(1400, 660)
X2 = [120, 800]
Y1b, Y2b = 70, 368
e.box("C", X2[0], Y1b, W, "C", "ConnectionRequest",
      [["+id: String", "+status: ConnectionStatus"]])
e.box("R", X2[1], Y1b, W, "C", "Review",
      [["+id: String", "+rating: Int", "+comment: String"],
       ["+createReview(): Review", "+canReview(): Boolean"]])
e.box("U", X2[0], Y2b, W, "C", "User",
      [["+id: String", "+email: String", "+role: Role"]])
e.box("RP", X2[1], Y2b, W, "C", "Report",
      [["+id: String", "+targetType: ReportTargetType", "+reason: ReportReason", "+status: ReportStatus"],
       ["+createReport(): Report", "+resolveReport(): Report"]])
e.edge([(560, 128), (680, 128), (680, 169), (800, 169)], label="ratedBy", m_start="1", m_end="0..2")
e.edge([(1000, 268), (1000, 330), (340, 330), (340, 368)], label="reviewer", m_start="0..*", m_end="1")
e.edge([(1060, 268), (1060, 352), (400, 352), (400, 368)], label="reviewee", m_start="0..*", m_end="1")
e.edge([(560, 426), (680, 426), (680, 480), (800, 480)], label="files", m_start="1", m_end="0..*")
e.edge([(340, 484), (340, 620), (1000, 620), (1000, 592)], label="resolves", m_start="1")
e._T(950, 600, "0..*", size=16)
e.save("E:/HOC TAP/my-project/ecosystem_ketnoi_giasu/docs/diagrams/class_c_trust")
