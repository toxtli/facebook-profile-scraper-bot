import sys
import time
import json
from pymongo import MongoClient
from SeleniumHelper import SeleniumHelper

class FacebookProfile(SeleniumHelper):

	db = None
	client = None
	credentials = None

	INITIAL_URL = 'https://www.facebook.com/'
	LOGIN_USER_PATH = '#email'
	LOGIN_PASS_PATH = '#pass'

	PROFILE_SECTION = {}
	PROFILE_CONTAINER = {}
	PROFILE_CONTENT = {}
	PROFILE_FIELD = {}

	PROFILE_SECTIONS = '[data-testid="info_section_left_nav"]'

	PROFILE_SECTION['OVERVIEW'] = PROFILE_SECTIONS + ' > li:nth-child(1) a'
	PROFILE_CONTAINER['OVERVIEW'] = '[data-pnref="overview"]'
	PROFILE_CONTENT['OVERVIEW'] = {}
	PROFILE_FIELD['OVERVIEW'] = {}

	PROFILE_CONTENT['OVERVIEW']['GENERAL'] = PROFILE_CONTAINER['OVERVIEW'] + ' > div:nth-child(1) .uiList li'
	PROFILE_FIELD['OVERVIEW']['GENERAL'] = {}
	PROFILE_FIELD['OVERVIEW']['GENERAL']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1)'}
	PROFILE_FIELD['OVERVIEW']['GENERAL']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'}

	PROFILE_CONTENT['OVERVIEW']['RIGHT'] = PROFILE_CONTAINER['OVERVIEW']+ ' > div:nth-child(2) .uiList li'
	PROFILE_FIELD['OVERVIEW']['RIGHT'] = {}
	PROFILE_FIELD['OVERVIEW']['RIGHT']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > span:nth-child(1)'}

	PROFILE_SECTION['EDUWORK'] = PROFILE_SECTIONS + ' > li:nth-child(2) a'
	PROFILE_CONTAINER['EDUWORK'] = '#pagelet_eduwork'
	PROFILE_CONTENT['EDUWORK'] = {}
	PROFILE_FIELD['EDUWORK'] = {}
	
	PROFILE_CONTENT['EDUWORK']['WORK'] = '[data-pnref="work"] li'
	PROFILE_FIELD['EDUWORK']['WORK'] = {}
	PROFILE_FIELD['EDUWORK']['WORK']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'}
	PROFILE_FIELD['EDUWORK']['WORK']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)'}
	PROFILE_FIELD['EDUWORK']['WORK']['INFO'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3)'}
	PROFILE_FIELD['EDUWORK']['WORK']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'}
	PROFILE_FIELD['EDUWORK']['WORK']['URL'] = {'attr':'href', 'type':'attr', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'}

	PROFILE_CONTENT['EDUWORK']['EDU'] = '[data-pnref="edu"] li'
	PROFILE_FIELD['EDUWORK']['EDU'] = {}
	PROFILE_FIELD['EDUWORK']['EDU']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'}
	PROFILE_FIELD['EDUWORK']['EDU']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)'}
	PROFILE_FIELD['EDUWORK']['EDU']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'}
	PROFILE_FIELD['EDUWORK']['EDU']['URL'] = {'attr':'href', 'type':'attr', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'}

	PROFILE_CONTENT['EDUWORK']['SKILLS'] = PROFILE_CONTAINER['EDUWORK'] + ' > div:nth-child(1) > div:not([data-pnref]) a'
	PROFILE_FIELD['EDUWORK']['SKILLS'] = {}
	PROFILE_FIELD['EDUWORK']['SKILLS']['NAME'] = {'type':'text', 'selector':''}
	# PROFILE_CONTENT_SKILLS = '[data-referrer="pagelet_eduwork"] .fbProfileEditExperiences li'

	PROFILE_SECTION['PLACES'] = PROFILE_SECTIONS + ' > li:nth-child(3) a'
	PROFILE_CONTAINER['PLACES'] = '#pagelet_hometown'
	PROFILE_CONTENT['PLACES'] = {}
	PROFILE_FIELD['PLACES'] = {}

	PROFILE_CONTENT['PLACES']['HOMETOWN'] = PROFILE_CONTAINER['PLACES'] + ' > div:nth-child(1) > div:nth-child(1) .uiList li'
	PROFILE_FIELD['PLACES']['HOMETOWN'] = {}
	PROFILE_FIELD['PLACES']['HOMETOWN']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > a:nth-child(1)'}
	PROFILE_FIELD['PLACES']['HOMETOWN']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'}
	PROFILE_FIELD['PLACES']['HOMETOWN']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'}
	PROFILE_FIELD['PLACES']['HOMETOWN']['URL'] = {'attr':'href', 'type':'attr', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > a:nth-child(1)'}
	
	PROFILE_CONTENT['PLACES']['OTHER'] = PROFILE_CONTAINER['PLACES'] + ' > div:nth-child(1) > div:nth-child(2) .uiList li'
	PROFILE_FIELD['PLACES']['OTHER'] = {}
	PROFILE_FIELD['PLACES']['OTHER']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > a:nth-child(1)'}
	PROFILE_FIELD['PLACES']['OTHER']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > a:nth-child(1)'}
	PROFILE_FIELD['PLACES']['OTHER']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'}
	PROFILE_FIELD['PLACES']['OTHER']['URL'] = {'attr':'href', 'type':'attr', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > a:nth-child(1)'}

	PROFILE_SECTION['CONTACT'] = PROFILE_SECTIONS + ' > li:nth-child(4) a'
	PROFILE_CONTAINER['CONTACT'] = '#pagelet_basic'
	PROFILE_CONTENT['CONTACT'] = {}
	PROFILE_FIELD['CONTACT'] = {}

	PROFILE_CONTENT['CONTACT']['ALL'] = '#pagelet_contact .fbProfileEditExperiences > li'
	PROFILE_FIELD['CONTACT']['ALL'] = {}
	PROFILE_FIELD['CONTACT']['ALL']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'}
	PROFILE_FIELD['CONTACT']['ALL']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1)'}
	PROFILE_FIELD['CONTACT']['ALL']['URL'] = {'attr':'href', 'type':'attr', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)'}

	PROFILE_CONTENT['CONTACT']['BASIC'] = PROFILE_CONTAINER['CONTACT'] + ' .fbProfileEditExperiences > li'
	PROFILE_FIELD['CONTACT']['BASIC'] = {}
	PROFILE_FIELD['CONTACT']['BASIC']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'}
	PROFILE_FIELD['CONTACT']['BASIC']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'}

	PROFILE_SECTION['RELATIONS'] = PROFILE_SECTIONS + ' > li:nth-child(5) a'
	PROFILE_CONTAINER['RELATIONS'] = '[data-pnref="family"]'
	PROFILE_CONTENT['RELATIONS'] = {}
	PROFILE_FIELD['RELATIONS'] = {}

	PROFILE_CONTENT['RELATIONS']['RELATIONSHIPS'] = '[data-pnref="rel"]'
	PROFILE_FIELD['RELATIONS']['RELATIONSHIPS'] = {}
	PROFILE_FIELD['RELATIONS']['RELATIONSHIPS']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'}
	PROFILE_FIELD['RELATIONS']['RELATIONSHIPS']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'}
	PROFILE_FIELD['RELATIONS']['RELATIONSHIPS']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'}
	PROFILE_FIELD['RELATIONS']['RELATIONSHIPS']['URL'] = {'attr':'href', 'type':'attr', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'}

	PROFILE_CONTENT['RELATIONS']['FAMILY'] = PROFILE_CONTAINER['RELATIONS'] + ' li'
	PROFILE_FIELD['RELATIONS']['FAMILY'] = {}
	PROFILE_FIELD['RELATIONS']['FAMILY']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)'}
	PROFILE_FIELD['RELATIONS']['FAMILY']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'}
	PROFILE_FIELD['RELATIONS']['FAMILY']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'}
	PROFILE_FIELD['RELATIONS']['FAMILY']['URL'] = {'attr':'href', 'type':'attr', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)'}

	PROFILE_SECTION['ABOUT'] = PROFILE_SECTIONS + ' > li:nth-child(6) a'
	PROFILE_CONTAINER['ABOUT'] = '#pagelet_bio'
	PROFILE_CONTENT['ABOUT'] = {}
	PROFILE_FIELD['ABOUT'] = {}

	PROFILE_CONTENT['ABOUT']['BIO'] = PROFILE_CONTAINER['ABOUT'] + ' li'
	PROFILE_FIELD['ABOUT']['BIO'] = {}
	PROFILE_FIELD['ABOUT']['BIO']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'}

	PROFILE_CONTENT['ABOUT']['QUOTES'] = '#pagelet_quotes li'
	PROFILE_FIELD['ABOUT']['QUOTES'] = {}
	PROFILE_FIELD['ABOUT']['QUOTES']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'}

	PROFILE_CONTENT['ABOUT']['PRONOUNCE'] = '#pagelet_pronounce li'
	PROFILE_FIELD['ABOUT']['PRONOUNCE'] = {}
	PROFILE_FIELD['ABOUT']['PRONOUNCE']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'}

	PROFILE_CONTENT['ABOUT']['NICKNAMES'] = '#pagelet_nicknames li'
	PROFILE_FIELD['ABOUT']['NICKNAMES'] = {}
	PROFILE_FIELD['ABOUT']['NICKNAMES']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > span:nth-child(1)'}

	PROFILE_SECTION['EVENTS'] = PROFILE_SECTIONS + ' > li:nth-child(7) a'
	PROFILE_CONTAINER['EVENTS'] = '[data-pnref="about"]'
	PROFILE_CONTENT['EVENTS'] = {}
	PROFILE_FIELD['EVENTS'] = {}

	PROFILE_CONTENT['EVENTS']['ALL_1'] = PROFILE_SECTION['EVENTS'] + ' > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(2) > li'
	PROFILE_FIELD['EVENTS']['ALL_1'] = {}
	PROFILE_FIELD['EVENTS']['ALL_1']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'}
	PROFILE_FIELD['EVENTS']['ALL_1']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > ul:nth-child(1)'}

	PROFILE_CONTENT['EVENTS']['ALL_2'] = PROFILE_SECTION['EVENTS'] + ' > li:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(2) > li'
	PROFILE_FIELD['EVENTS']['ALL_2'] = {}
	PROFILE_FIELD['EVENTS']['ALL_2']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'}
	PROFILE_FIELD['EVENTS']['ALL_2']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > ul:nth-child(1)'}

	GENERAL = {}
	GENERAL['NAME'] = {'type':'text', 'selector':'#fb-timeline-cover-name'}
	GENERAL['MUTUAL'] = {'type':'text', 'selector':'#fbTimelineHeadline > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(3) > span:nth-child(1) > span:nth-child(1)'}

	SEE_ALL = '[data-referrer="timeline_collections_overview_see_all"]'

	CONTAINER_ABOUT = '#pagelet_timeline_medley_about'

	CONTAINER = {}
	ITEMS = {}
	DATA = {}

	CONTAINER['FRIENDS'] = '#pagelet_timeline_medley_friends'
	ITEMS['FRIENDS'] = CONTAINER['FRIENDS'] + ' li'
	DATA['FRIENDS'] = {}
	DATA['FRIENDS']['ID'] = {'attr':'data-profileid', 'type':'attr', 'selector':'[data-profileid]'}
	DATA['FRIENDS']['NAME'] = {'type':'text', 'selector':'.uiProfileBlockContent > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'} # text
	DATA['FRIENDS']['STATUS'] = {'type':'text', 'selector':'.uiProfileBlockContent > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > a:nth-child(2)'} # text
	DATA['FRIENDS']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'div:nth-child(1) > a:nth-child(1) > img:nth-child(1)'} # src

	CONTAINER['PHOTOS'] = '#pagelet_timeline_medley_photos'
	ITEMS['PHOTOS'] = CONTAINER['PHOTOS'] + ' .fbPhotoStarGridElement'
	DATA['PHOTOS'] = {}
	DATA['PHOTOS']['ID'] = {'attr':'data-fbid', 'type':'attr', 'selector':'[data-fbid]'} # data-fbid
	DATA['PHOTOS']['IMAGE'] = {'attr':'background-image', 'type':'style', 'selector':'.uiMediaThumbImg'} # background-image
	DATA['PHOTOS']['LIKES'] = {'type':'text', 'selector':'div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1)'} # text
	DATA['PHOTOS']['COMMENTS'] = {'type':'text', 'selector':'div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1)'} # text

	CONTAINER['VIDEOS'] = '#pagelet_timeline_medley_videos'
	ITEMS['VIDEOS'] = CONTAINER['VIDEOS'] + ' .fbPhotoStarGridElement'
	DATA['VIDEOS'] = {}
	DATA['VIDEOS']['ID'] = {'attr':'data-fbid', 'type':'attr', 'selector':'[data-fbid]'} # data-fbid
	DATA['VIDEOS']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.uiScaledImageContainer'} # src
	DATA['VIDEOS']['DURATION'] = {'type':'text', 'selector':'[rel="theater"] > span:nth-child(1) > div:nth-child(3)'} # text

	CONTAINER['MAP'] = '#pagelet_timeline_medley_map'
	ITEMS['MAP'] = CONTAINER['MAP'] + ' li'
	DATA['MAP'] = {}
	DATA['MAP']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.uiScaledImageContainer'} # src
	DATA['MAP']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'} # text
	DATA['MAP']['URL'] = {'attr':'href', 'type':'attr', 'selector':'div:nth-child(1) > a:nth-child(1)'} # href

	CONTAINER['MUSIC'] = '#pagelet_timeline_medley_music'
	ITEMS['MUSIC'] = CONTAINER['MUSIC'] + ' li'
	DATA['MUSIC'] = {}
	DATA['MUSIC']['ID'] = {'attr':'data-obj', 'type':'attr', 'selector':'[data-obj]'} # data-obj
	DATA['MUSIC']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.music_artwork'} # src
	DATA['MUSIC']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'} # text
	DATA['MUSIC']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'} # text
	DATA['MUSIC']['URL'] = {'attr':'href', 'type':'attr', 'selector':'.music_play_button a'} # href

	CONTAINER['MOVIES'] = '#pagelet_timeline_medley_movies'
	ITEMS['MOVIES'] = CONTAINER['MOVIES'] + ' li'
	DATA['MOVIES'] = {}
	DATA['MOVIES']['ID'] = {'attr':'data-obj', 'type':'attr', 'selector':'[data-obj]'} # data-obj
	DATA['MOVIES']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['MOVIES']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'} # text
	DATA['MOVIES']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'} # text

	CONTAINER['TV'] = '#pagelet_timeline_medley_tv'
	ITEMS['TV'] = CONTAINER['TV'] + ' li'
	DATA['TV'] = {}
	DATA['TV']['ID'] = {'attr':'data-obj', 'type':'attr', 'selector':'[data-obj]'} # data-obj
	DATA['TV']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['TV']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'} # text
	DATA['TV']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'} # text

	CONTAINER['BOOKS'] = '#pagelet_timeline_medley_books'
	ITEMS['BOOKS'] = CONTAINER['BOOKS'] + ' li'
	DATA['BOOKS'] = {}
	DATA['BOOKS']['ID'] = {'attr':'data-obj', 'type':'attr', 'selector':'[data-obj]'} # data-obj
	DATA['BOOKS']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['BOOKS']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'} # text
	DATA['BOOKS']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'} # text

	CONTAINER['GAMES'] = '#pagelet_timeline_medley_games'
	ITEMS['GAMES'] = CONTAINER['GAMES'] + ' li'
	DATA['GAMES'] = {}
	DATA['GAMES']['ID'] = {'attr':'data-obj', 'type':'attr', 'selector':'[data-obj]'} # data-obj
	DATA['GAMES']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['GAMES']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'} # text
	DATA['GAMES']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'} # text

	CONTAINER['EVENTS'] = '#pagelet_timeline_medley_events'
	ITEMS['EVENTS'] = CONTAINER['EVENTS'] + ' li'
	DATA['EVENTS'] = {}
	DATA['EVENTS']['ID'] = {'attr':'data-collection-item', 'type':'attr', 'selector':'[data-collection-item]'} # data-collection-item
	DATA['EVENTS']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['EVENTS']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > a:nth-child(1)'} # text
	DATA['EVENTS']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)'} # text

	CONTAINER['LIKES'] = '#pagelet_timeline_medley_likes'
	ITEMS['LIKES'] = CONTAINER['LIKES'] + ' li'
	DATA['LIKES'] = {}
	DATA['LIKES']['ID'] = {'attr':'data-profileid', 'type':'attr', 'selector':'[data-profileid]'} # data-profileid
	DATA['LIKES']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['LIKES']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'} # text
	DATA['LIKES']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'} # text

	CONTAINER['GROUPS'] = '#pagelet_timeline_medley_groups'
	ITEMS['GROUPS'] = CONTAINER['GROUPS'] + ' li'
	DATA['GROUPS'] = {}
	DATA['GROUPS']['ID'] = {'attr':'data-collection-item', 'type':'attr', 'selector':'[data-collection-item]'} # data-collection-item
	DATA['GROUPS']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'} # text
	DATA['GROUPS']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(3)'} # text
	DATA['GROUPS']['MEMBERS'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)'} # text

	CONTAINER['REVIEWS'] = '#pagelet_timeline_medley_reviews'
	ITEMS['REVIEWS'] = CONTAINER['REVIEWS'] + ' li'
	DATA['REVIEWS'] = {}
	DATA['REVIEWS']['ID'] = {'attr':'data-collection-item', 'type':'attr', 'selector':'[data-collection-item]'} # data-collection-item
	DATA['REVIEWS']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['REVIEWS']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1) > a:nth-child(1)'} # text
	DATA['REVIEWS']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(2)'} # text
	DATA['REVIEWS']['STARS'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > i:nth-child(1) > u:nth-child(1)'} # text

	CONTAINER['SPORTS'] = '#pagelet_timeline_medley_sports'
	ITEMS['SPORTS'] = CONTAINER['SPORTS'] + ' li'
	DATA['SPORTS'] = {}
	DATA['SPORTS']['ID'] = {'attr':'data-obj', 'type':'attr', 'selector':'[data-obj]'} # data-obj
	DATA['SPORTS']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['SPORTS']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'} # text

	CONTAINER['PINTEREST'] = '#pagelet_timeline_medley_app_pinterestapp'
	ITEMS['PINTEREST'] = CONTAINER['PINTEREST'] + ' li'
	DATA['PINTEREST'] = {}
	DATA['PINTEREST']['ID'] = {'attr':'data-obj', 'type':'attr', 'selector':'[data-obj]'} # data-obj
	DATA['PINTEREST']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['PINTEREST']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'} # text
	DATA['PINTEREST']['DESCRIPTION'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)'} # text

	CONTAINER['INSTAGRAM'] = '#pagelet_timeline_medley_app_instapp'
	ITEMS['INSTAGRAM'] = CONTAINER['INSTAGRAM'] + ' li'
	DATA['INSTAGRAM'] = {}
	DATA['INSTAGRAM']['ID'] = {'attr':'data-obj', 'type':'attr', 'selector':'[data-obj]'} # data-obj
	DATA['INSTAGRAM']['IMAGE'] = {'attr':'src', 'type':'attr', 'selector':'.img'} # src
	DATA['INSTAGRAM']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)'} # text
	DATA['INSTAGRAM']['LIKES'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > form:nth-child(1) > div:nth-child(5) > span:nth-child(2) > a:nth-child(1) > span:nth-child(1) > span:nth-child(2)'} # text
	DATA['INSTAGRAM']['COMMENTS'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > form:nth-child(1) > div:nth-child(5) > span:nth-child(2) > a:nth-child(1) > span:nth-child(2) > span:nth-child(2)'} # text

	TIMELINE_MESSAGES = '[data-insertion-position]'
	TIMELINE = {}
	TIMELINE['MESSAGES'] = {}
	TIMELINE['MESSAGES']['NAME'] = {'type':'text', 'selector':'div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h5:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > a:nth-child(1)'}
	TIMELINE['MESSAGES']['DATE'] = {'type':'text', 'selector':'.timestampContent'}
	TIMELINE['MESSAGES']['DESCRIPTION'] = {'type':'text', 'selector':'.userContent'}

	users = {}

	def login(self):
		self.loadPage(self.INITIAL_URL)
		self.selectAndWrite(self.LOGIN_USER_PATH, self.credentials['email'])
		self.submitForm(self.selectAndWrite(self.LOGIN_PASS_PATH, self.credentials['password']))

	def extractProfiles(self, profiles):
		print 'Logging in'
		self.login()
		print 'Extracting profiles'
		for profileId in profiles:
			self.openProfile(profileId)
			self.scrollingDown(6)
			self.extractMessages(profileId)
			self.extractProfile(profileId)
			self.scrollingDown(20)
			# self.expandAll()
			self.getContainers(profileId)
			try:
				self.db.profiles.insert_one(self.users[profileId])
			except:
				print sys.exc_info()
		self.close()
		return self.users

	def expandAll(self):
		cont = 0
		for key in self.CONTAINER:
			if key != 'GROUPS':
				section = self.getElement(self.CONTAINER[key])
				if section:
					seeAllButton = self.getElementFrom(section, self.SEE_ALL)
					if seeAllButton:
						try:
							self.click(seeAllButton)
							time.sleep(1)
						except:
							pass

	def openProfile(self, profileId):
		self.users[profileId] = {}
		self.users[profileId]['_id'] = profileId
		self.users[profileId]['profileId'] = profileId
		self.users[profileId]['profileImage'] = 'http://graph.facebook.com/' + profileId + '/picture?type=large'
		self.loadPage(self.INITIAL_URL + profileId)
		userUrl = self.driver.current_url
		arrUrl = userUrl.split(self.INITIAL_URL)
		userId = arrUrl[1]
		self.users[profileId]['userName'] = userId
		for field in self.GENERAL:
			record = self.GENERAL[field]
			self.users[profileId][field] = self.getFieldValue(record)

	def getFieldValue(self, record, parent=None):
		exit = None
		if parent:
			if record['type'] == 'attr':
				exit = self.getElementFromAttribute(parent, record['selector'], record['attr'])
			elif record['type'] == 'text':
				exit = self.getElementFromValue(parent, record['selector'])
			elif record['type'] == 'style':
				exit = record['attr']
		else:
			if record['type'] == 'attr':
				exit = self.getElementAttribute(record['selector'], record['attr'])
			elif record['type'] == 'text':
				exit = self.getElementValue(record['selector'])
			elif record['type'] == 'style':
				exit = record['attr']
		return exit

	def extractProfile(self, profileId):
		try:
			aboutURL = self.INITIAL_URL + self.users[profileId]['userName'] + '/about'
			self.loadPage(aboutURL)
			self.waitShowElement(self.PROFILE_SECTIONS, self.WAIT)
			for section in self.PROFILE_SECTION:
				nextOption = self.getElement(self.PROFILE_SECTION[section])
				self.click(nextOption)
				self.waitShowElement(self.PROFILE_CONTAINER[section], self.WAIT)
				self.users[profileId][section] = {}
				for subsection in self.PROFILE_CONTENT[section]:
					self.users[profileId][section][subsection] = []
					elements = self.getElements(self.PROFILE_CONTENT[section][subsection])
					for element in elements:
						row = {}
						for field in self.PROFILE_FIELD[section][subsection]:
							record = self.PROFILE_FIELD[section][subsection][field]
							row[field] = self.getFieldValue(record, element)
						self.users[profileId][section][subsection].append(row)
		except:
			print sys.exc_info()
			return False

	def getContainers(self, profileId):
		for category in self.CONTAINER.keys():
			self.users[profileId][category] = []
			elements = self.getElements(self.ITEMS[category])
			for element in elements:
				row = {}
				for field in self.DATA[category].keys():
					record = self.DATA[category][field]
					row[field] = self.getFieldValue(record, element)
				self.users[profileId][category].append(row)

	def extractMessages(self, profileId):
		self.waitShowElement(self.TIMELINE_MESSAGES, self.WAIT)
		elements = self.getElements(self.TIMELINE_MESSAGES)
		for category in self.TIMELINE:
			self.users[profileId][category] = []
			for element in elements:
				row = {}
				for field in self.TIMELINE[category]:
					record = self.TIMELINE[category][field]
					row[field] = self.getFieldValue(record, element)
				self.users[profileId][category].append(row)

	def __init__(self, credentials): 
		super(self.__class__, self).__init__()
		self.client = MongoClient()
		self.db = self.client['test']
		self.credentials = credentials