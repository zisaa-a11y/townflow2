class UserRole:
    ADMIN = "admin"
    MODERATOR = "moderator"
    CITIZEN = "citizen"
    VOLUNTEER = "volunteer"

    CHOICES = (
        (ADMIN, "Admin"),
        (MODERATOR, "Moderator"),
        (CITIZEN, "Citizen"),
        (VOLUNTEER, "Volunteer"),
    )


class OtpChannel:
    EMAIL = "email"
    PHONE = "phone"

    CHOICES = (
        (EMAIL, "Email"),
        (PHONE, "Phone"),
    )


class AlertType:
    BLOOD_REQUEST = "bloodRequest"
    EVENT_REMINDER = "eventReminder"
    COMMUNITY_ALERT = "communityAlert"
    REPORT_UPDATE = "reportUpdate"

    CHOICES = (
        (BLOOD_REQUEST, "Blood Request"),
        (EVENT_REMINDER, "Event Reminder"),
        (COMMUNITY_ALERT, "Community Alert"),
        (REPORT_UPDATE, "Report Update"),
    )


class FileCategory:
    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ARCHIVE = "archive"
    OTHER = "other"

    CHOICES = (
        (DOCUMENT, "Document"),
        (IMAGE, "Image"),
        (VIDEO, "Video"),
        (AUDIO, "Audio"),
        (ARCHIVE, "Archive"),
        (OTHER, "Other"),
    )


class FeedCategory:
    NEWS = "news"
    ALERT = "alert"
    EVENT = "event"

    CHOICES = (
        (NEWS, "News"),
        (ALERT, "Alert"),
        (EVENT, "Event"),
    )


class JobType:
    FULL_TIME = "fullTime"
    PART_TIME = "partTime"
    REMOTE = "remote"

    CHOICES = (
        (FULL_TIME, "Full Time"),
        (PART_TIME, "Part Time"),
        (REMOTE, "Remote"),
    )


class IssueType:
    ROAD = "road"
    WATER = "water"
    ELECTRICITY = "electricity"
    WASTE = "waste"
    OTHER = "other"

    CHOICES = (
        (ROAD, "Road"),
        (WATER, "Water"),
        (ELECTRICITY, "Electricity"),
        (WASTE, "Waste"),
        (OTHER, "Other"),
    )


class ReportStatus:
    PENDING = "pending"
    IN_PROGRESS = "inProgress"
    RESOLVED = "resolved"

    CHOICES = (
        (PENDING, "Pending"),
        (IN_PROGRESS, "In Progress"),
        (RESOLVED, "Resolved"),
    )


class EventCategory:
    FESTIVAL = "festival"
    WORKSHOP = "workshop"
    SPORTS = "sports"
    CULTURAL = "cultural"

    CHOICES = (
        (FESTIVAL, "Festival"),
        (WORKSHOP, "Workshop"),
        (SPORTS, "Sports"),
        (CULTURAL, "Cultural"),
    )


class LibraryCategory:
    BOOK = "book"
    ARTICLE = "article"
    VIDEO = "video"

    CHOICES = (
        (BOOK, "Book"),
        (ARTICLE, "Article"),
        (VIDEO, "Video"),
    )


class BloodRequestUrgency:
    NORMAL = "normal"
    URGENT = "urgent"

    CHOICES = (
        (NORMAL, "Normal"),
        (URGENT, "Urgent"),
    )


class BloodRequestStatus:
    PENDING = "pending"
    MATCHED = "matched"
    FULFILLED = "fulfilled"

    CHOICES = (
        (PENDING, "Pending"),
        (MATCHED, "Matched"),
        (FULFILLED, "Fulfilled"),
    )


class VolunteerStatus:
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"

    CHOICES = (
        (UPCOMING, "Upcoming"),
        (ACTIVE, "Active"),
        (COMPLETED, "Completed"),
    )
