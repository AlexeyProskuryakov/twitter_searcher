#__author__ = 'Alesha'

#

##Friends & Followers

##Users follow their interests on Twitter through both one-way and mutual following relationships.

#

##Resource	 Description

##GET

get_followers_ids = "followers/ids"

## #Returns an array of numeric IDs for every user following the specified user.

## This method is powerful when used in conjunction with users/lookup.

##GET

get_friends_ids = "friends/ids"

##Returns an array of numeric IDs for every user the specified user is following.

## This method is powerful when used in conjunction with users/lookup.

#

##GET

get_friends_ship_exist = 'friendships/exists'
##	 Test for the existence of friendship between two users.
## Will return true if user_a follows user_b, otherwise will return false.
## Authentication is required if either user A or user
## B are protected. Additionally the authenticating user must be a follower of the protected user. Consider using...

#GET,Returns an array of numeric IDs for every user who has a pending request to follow the authenticating user
friendships_incoming = 'friendships/incoming'

#GET,Returns an array of numeric IDs for every protected user for whom the authenticating user has a pending follow request
friendships_outgoing = 'friendships/outgoing'

#GET,Returns detailed information about the relationship between two users
friendships_show = 'friendships/show'
#POST,Allows the authenticating users to follow the user specified in the ID parameter Returns the befriended user in the requested format when successful Returns a string describing the failure condition when unsuccessful If you are already friends with the user a HTTP 403 may be returned though for
friendships_create = 'friendships/create'
#POST,Allows the authenticating users to unfollow the user specified in the ID parameter Returns the unfollowed user in the requested format when successful Returns a string describing the failure condition when unsuccessful
friendships_destroy = 'friendships/destroy'
#GET,Returns the relationship of the authenticating user to the comma separated list of up to 100 screen names or user ids provided Values for connections can be following following requested followed by none
friendships_lookup = 'friendships/lookup'
#POST,Allows one to enable or disable retweets and device notifications from the specified user
friendships_update = 'friendships/update'
#GET,retweet ids Returns an array of user ids that the currently authenticated user does not want to see retweets from
friendships_no = 'friendships/no'
#Users,at the center of everything Twitter they follow they favorite and tweet retweet
are = 'are'
#GET,Return up to 100 users worth of extended information specified by either ID screen name or combination of the two The author s most recent status if the authenticating user has permission will be returned inline This method is crucial for consumers of the Streaming API It s also well suited
users_lookup = 'users/lookup'
#GET,image/ screen name Access the profile image in various sizes for the user with the indicated screen name If no size is provided the normal image is returned This resource does not return JSON or XML but instead returns a 302 redirect to the actual image resource This method should only be used by application
users_profile = 'users/profile'
#GET,Runs a search for users similar to Find People button on Twitter com The results returned by people search on Twitter com are the same as those returned by this API request Note that unlike GET search this method does not support any operators Only the first 1000 matches are available
users_search = 'users/search'
#GET,Returns extended information of a given user specified by ID or screen name as per the required id parameter The author s most recent status will be returned inline
users_show = 'users/show'
#GET,Returns an array of users that the specified user can contribute to
users_contributees = 'users/contributees'
#GET,Returns an array of users who can contribute to the specified account
users_contributors = 'users/contributors'
#Categorical,of users that others may be interested to follow
organization = 'organization'
#GET,Access to Twitter s suggested user list This returns the list of suggested user categories The category can be used in GET users/suggestions/ slug to get the users in that category
users_suggestions = 'users/suggestions'
#GET,slug Access the users in a given category of the Twitter suggested user list It is recommended that end clients cache this data for no more than one hour
users_suggestions = 'users/suggestions/'
#GET,slug/members format Access the users in a given category of the Twitter suggested user list and return their most recent status if they are not a protected user
users_suggestions = 'users/suggestions/'
#Users,tweets to give recognition to awesome tweets to curate the best of Twitter to save for reading later and a variety of other reasons Likewise developers make use of favs in many different ways
favorite = 'favorite'
#GET,Returns the 20 most recent favorite statuses for the authenticating or specified user in the requested format
favorites = 'favorites'
#POST,id Favorites the status specified in the ID parameter as the authenticating user Returns the favorite status when successful This process invoked by this method is asynchronous The immediately returned status may not indicate the resultant favorited status of the tweet A 200 OK response from this
favorites_create = 'favorites/create/'
#POST,id Un favorites the status specified in the ID parameter as the authenticating user Returns the un favorited status in the requested format when successful This process invoked by this method is asynchronous The immediately returned status may not indicate the resultant favorited status of the
favorites_destroy = 'favorites/destroy/'
#Lists,collections of tweets culled from a curated list of Twitter users List timeline methods include tweets by all members of a list
are = 'are'
#GET,Returns all lists the authenticating or specified user subscribes to including their own The user is specified using the user id or screen name parameters If no user is given the authenticating user is used
lists_all = 'lists/all'
#GET,Returns tweet timeline for members of the specified list Historically retweets were not available in list timeline responses but you can now use the include rts true parameter to additionally receive retweet objects
lists_statuses = 'lists/statuses'
#POST,Removes the specified member from the list The authenticated user must be the list s owner to remove members from the list
lists_members_destroy = 'lists/members/destroy'
#GET,Returns the lists the specified user has been added to If user id or screen name are not provided the memberships for the authenticating user are returned
lists_memberships = 'lists/memberships'
#GET,Returns the subscribers of the specified list Private list subscribers will only be shown if the authenticated user owns the specified list
lists_subscribers = 'lists/subscribers'
#POST,Subscribes the authenticated user to the specified list
lists_subscribers_create = 'lists/subscribers/create'
#GET,Check if the specified user is a subscriber of the specified list Returns the user if they are subscriber
lists_subscribers_show = 'lists/subscribers/show'
#POST,Unsubscribes the authenticated user from the specified list
lists_subscribers_destroy = 'lists/subscribers/destroy'
#POST,all Adds multiple members to a list by specifying a comma separated list of member ids or screen names The authenticated user must own the list to be able to add members to it Note that lists can t have more than 500 members and you are limited to adding up to 100 members to a list at a time with
lists_members_create = 'lists/members/create'
#GET,Check if the specified user is a member of the specified list
lists_members_show = 'lists/members/show'
#GET,Returns the members of the specified list Private list members will only be shown if the authenticated user owns the specified list
lists_members = 'lists/members'
#POST,Add a member to a list The authenticated user must own the list to be able to add members to it Note that lists can t have more than 500 members
lists_members_create = 'lists/members/create'
#POST,Deletes the specified list The authenticated user must own the list to be able to destroy it
lists_destroy = 'lists/destroy'
#POST,Updates the specified list The authenticated user must own the list to be able to update it
lists_update = 'lists/update'
#POST,Creates a new list for the authenticated user Note that you can t create more than 20 lists per account
lists_create = 'lists/create'
#GET,Returns the lists of the specified or authenticated user Private lists will be included if the authenticated user is the same as the user whose lists are being returned
lists = 'lists'
#GET,Returns the specified list Private lists will only be shown if the authenticated user owns the specified list
lists_show = 'lists/show'
#GET,Obtain a collection of the lists the specified user is subscribed to 20 lists per page by default Does not include the user s own lists
lists_subscriptions = 'lists/subscriptions'
#POST,all Removes multiple members from a list by specifying a comma separated list of member ids or screen names The authenticated user must own the list to be able to remove members from it Note that lists can t have more than 500 members and you are limited to removing up to 100 members to a list at a
lists_members_destroy = 'lists/members/destroy'
#Account,configuration settings for users
level = 'level'
#GET,limit status Returns the remaining number of API requests available to the requesting user before the API limit is reached for the current hour Calls to rate limit status do not count against the rate limit If authentication credentials are provided the rate limit status for the authenticating user is
account_rate = 'account/rate'
#GET,credentials Returns an HTTP 200 OK response code and a representation of the requesting user if authentication was successful returns a 401 status code and an error message if not Use this method to test if supplied user credentials are valid
account_verify = 'account/verify'
#POST,session Ends the session of the authenticating user returning a null cookie Use this method to sign users out of client facing applications like widgets
account_end = 'account/end'
#POST,profile Sets values that users are able to set under the Account tab of their settings page Only the parameters specified will be updated
account_update = 'account/update'
#POST,profile background image Updates the authenticating user s profile background image This method can also be used to enable or disable the profile background image Although each parameter is marked as optional at least one of image tile or use must be provided when making this request
account_update = 'account/update'
#POST,profile colors Sets one or more hex values that control the color scheme of the authenticating user s profile page on twitter com Each parameter s value must be a valid hexidecimal value and may be either three or six characters ex fff or ffffff
account_update = 'account/update'
#POST,profile image Updates the authenticating user s profile image Note that this method expects raw multipart data not a URL to an image This method asynchronously processes the uploaded file before updating the user s profile image URL You can either update your local cache the next time you request the user s
account_update = 'account/update'
#GET,Returns the current count of friends followers updates statuses and favorites of the authenticating user
account_totals = 'account/totals'
#GET,Returns settings including current trend geo and sleep time information for the authenticating user
account_settings = 'account/settings'
#POST,Updates the authenticating user s settings
account_settings = 'account/settings'
