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
        logger.debug(">>> Entering __init__(user=%s)", user)
        db.Model.__init__(self, user=user, **kwargs)
        logger.debug("<<< Exiting __init__(user=%s)", user)

    def is_following(self, profile):
        logger.debug(">>> Entering is_following(profile=%s)", profile)
        import time; __log_start = time.time()
        logger.debug("<<< Exiting is_following(profile=%s)", profile)
        logger.info("is_following(profile)=%s: count operation took %s ms", profile, int((time.time() - __log_start) * 1000))
        return bool(self.follows.filter(followers_assoc.c.followed_by == profile.id).count())

    def follow(self, profile):
        logger.debug(">>> Entering follow(profile=%s)", profile)
        if self is not profile and not self.is_following(profile):
            self.follows.append(profile)
            return True
        logger.debug("<<< Exiting follow(profile=%s)", profile)
        return False

    def unfollow(self, profile):
        logger.debug(">>> Entering unfollow(profile=%s)", profile)
        if self is not profile and self.is_following(profile):
            self.follows.remove(profile)
            return True
        logger.debug("<<< Exiting unfollow(profile=%s)", profile)
        return False

    @property
    def following(self):
        logger.debug(">>> Entering following()")
        if current_user:
            return current_user.profile.is_following(self)
        logger.debug("<<< Exiting following()")
        return False

    @property
    def username(self):
        logger.debug(">>> Entering username()")
        logger.debug("<<< Exiting username()")
        return self.user.username

    @property
    def bio(self):
        logger.debug(">>> Entering bio()")
        logger.debug("<<< Exiting bio()")
        return self.user.bio

    @property
    def image(self):
        logger.debug(">>> Entering image()")
        logger.debug("<<< Exiting image()")
        return self.user.image

    @property
    def email(self):
        logger.debug(">>> Entering email()")
        logger.debug("<<< Exiting email()")
        return self.user.email
