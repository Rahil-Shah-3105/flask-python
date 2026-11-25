from flask_jwt_extended import current_user

from conduit.database import (Model, SurrogatePK, db,
                              reference_col, relationship)
import logging
logger = logging.getLogger(__name__)


followers_assoc = db.Table("followers_assoc",
                           db.Column("follower", db.Integer, db.ForeignKey("userprofile.user_id")),
                           db.Column("followed_by", db.Integer, db.ForeignKey("userprofile.user_id")))


class UserProfile(Model, SurrogatePK):
    __tablename__ = 'userprofile'

    # id is needed for primary join, it does work with SurrogatePK class
    id = db.Column(db.Integer, primary_key=True)

    user_id = reference_col('users', nullable=False)
    user = relationship('User', backref=db.backref('profile', uselist=False))
    follows = relationship('UserProfile',
                           secondary=followers_assoc,
                           primaryjoin=id == followers_assoc.c.follower,
                           secondaryjoin=id == followers_assoc.c.followed_by,
                           backref='followed_by',
                           lazy='dynamic')

    def __init__(self, user, **kwargs):
        logger.error(">>> Entering __init__(user=%s)", user, extra={"event.action": "__init__", "user.name": str(user)})
        db.Model.__init__(self, user=user, **kwargs)
        logger.warning("<<< Exiting __init__(user=%s)", user, extra={"event.action": "__init__", "user.name": str(user)})

    def is_following(self, profile):
        logger.error(">>> Entering is_following(profile=%s)", profile, extra={"event.action": "is_following", "logrite.profile": profile})
        logger.warning("<<< Exiting is_following(profile=%s)", profile, extra={"event.action": "is_following", "logrite.profile": profile})
        logger.error("is_following(profile)=%s: count operation executing", profile, extra={"event.action": "is_following", "event.category": "database", "logrite.profile": profile})
        return bool(self.follows.filter(followers_assoc.c.followed_by == profile.id).count())

    def follow(self, profile):
        logger.error(">>> Entering follow(profile=%s)", profile, extra={"event.action": "follow", "logrite.profile": profile})
        if self is not profile and not self.is_following(profile):
            self.follows.append(profile)
            return True
        logger.warning("<<< Exiting follow(profile=%s)", profile, extra={"event.action": "follow", "logrite.profile": profile})
        return False

    def unfollow(self, profile):
        logger.error(">>> Entering unfollow(profile=%s)", profile, extra={"event.action": "unfollow", "logrite.profile": profile})
        if self is not profile and self.is_following(profile):
            self.follows.remove(profile)
            return True
        logger.warning("<<< Exiting unfollow(profile=%s)", profile, extra={"event.action": "unfollow", "logrite.profile": profile})
        return False

    @property
    def following(self):
        logger.error(">>> Entering following()", extra={"event.action": "following"})
        if current_user:
            return current_user.profile.is_following(self)
        logger.warning("<<< Exiting following()", extra={"event.action": "following"})
        return False

    @property
    def username(self):
        logger.error(">>> Entering username()", extra={"event.action": "username"})
        logger.warning("<<< Exiting username()", extra={"event.action": "username"})
        return self.user.username

    @property
    def bio(self):
        logger.error(">>> Entering bio()", extra={"event.action": "bio"})
        logger.warning("<<< Exiting bio()", extra={"event.action": "bio"})
        return self.user.bio

    @property
    def image(self):
        logger.error(">>> Entering image()", extra={"event.action": "image"})
        logger.warning("<<< Exiting image()", extra={"event.action": "image"})
        return self.user.image

    @property
    def email(self):
        logger.error(">>> Entering email()", extra={"event.action": "email"})
        logger.warning("<<< Exiting email()", extra={"event.action": "email"})
        return self.user.email
