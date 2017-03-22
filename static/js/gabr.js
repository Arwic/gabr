var global_profile_card;
var global_view_post;
var cursorX;
var cursorY;
var post_time_oldest;
var post_time_newest;

const INT_MAX = 2147483647;

$.ajaxSetup({
    headers: {"X-CSRFToken": getCookie("csrftoken")}
});

$(document).ready(function () {
    global_view_post = $("#modal-viewpost");
    global_profile_card = $("#global-profile-card");

    $(document).mousemove(function (event) {
        cursorX = event.pageX;
        cursorY = event.pageY;
    });

    global_view_post.on("hidden.bs.modal", function () {
        var re = /\/post\/([1-9]+)/;
        if (!window.location.pathname.search(re))
            window.location.pathname = "/";
    });

    global_profile_card.mouseleave(function () {
        $(this).hide();
    });

    updateNotificationCount();
    updateTrends();
});

function guid() {
    var d = new Date().getTime();
    var id = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == "x" ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return id;
}

// http://stackoverflow.com/a/499158/3105105
function setSelectionRange(input, selectionStart, selectionEnd) {
    if (input.setSelectionRange) {
        input.focus();
        input.setSelectionRange(selectionStart, selectionEnd);
    }
    else if (input.createTextRange) {
        var range = input.createTextRange();
        range.collapse(true);
        range.moveEnd('character', selectionEnd);
        range.moveStart('character', selectionStart);
        range.select();
    }
}

// http://stackoverflow.com/a/841121/3105105
$.fn.selectRange = function(start, end) {
    if(end === undefined) {
        end = start;
    }
    return this.each(function() {
        if('selectionStart' in this) {
            this.selectionStart = start;
            this.selectionEnd = end;
        } else if(this.setSelectionRange) {
            this.setSelectionRange(start, end);
        } else if(this.createTextRange) {
            var range = this.createTextRange();
            range.collapse(true);
            range.moveEnd('character', end);
            range.moveStart('character', start);
            range.select();
        }
    });
};

function getCookie(cookieName) {
    if (document.cookie.length > 0) {
        var c_start = document.cookie.indexOf(cookieName + "=");
        if (c_start != -1) {
            c_start = c_start + cookieName.length + 1;
            var c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

// --------------- NYI ajax code (functions like these dont work due to how events work but the code can be used later) ---------------

function ajaxFeedUserPosts(target_username) {
    $.ajax({
        url: "/ajax/get/user-posts/",
        type: "POST",
        data: {
            "username": target_username,
            "time-oldest": post_time_oldest,
            "time-newest": post_time_newest
        },
        dataType: "json",
        success: function (data) {
            post_time_oldest = data["time-oldest"];
            post_time_newest = data["time-newest"];
        },
        failure: function (data) {
            console.log("Unable to load user post feed");
        }
    });
}

function ajaxFeedUserFollowers(target_username) {
    $.ajax({
        url: "/ajax/get/user-followers/",
        type: "POST",
        data: {
            "username": target_username,
            "time-oldest": post_time_oldest,
            "time-newest": post_time_newest
        },
        dataType: "json",
        success: function (data) {
            post_time_oldest = data["time-oldest"];
            post_time_newest = data["time-newest"];
        },
        failure: function (data) {
            console.log("Unable to user follower feed");
        }
    });
}

function ajaxFeedUserFollows(target_username) {
    $.ajax({
        url: "/ajax/get/user-follows/",
        type: "POST",
        data: {
            "username": target_username,
            "time-oldest": post_time_oldest,
            "time-newest": post_time_newest
        },
        dataType: "json",
        success: function (data) {
            post_time_oldest = data["time-oldest"];
            post_time_newest = data["time-newest"];
        },
        failure: function (data) {
            console.log("Unable to user follows feed");
        }
    });
}

function ajaxFeedUserLikes(target_username) {
    $.ajax({
        url: "/ajax/get/user-likes/",
        type: "POST",
        data: {
            "username": target_username,
            "time-oldest": post_time_oldest,
            "time-newest": post_time_newest
        },
        dataType: "json",
        success: function (data) {
            post_time_oldest = data["time-oldest"];
            post_time_newest = data["time-newest"];
        },
        failure: function (data) {
            console.log("Unable to user likes feed");
        }
    });
}

function ajaxCommandReportPost(post_id) {
    $.ajax({
        url: "/ajax/command/report-post/",
        type: "POST",
        data: {
            "post-id": post_id
        },
        dataType: "json",
        success: function (data) {
        },
        failure: function (data) {
            console.log("Unable to report post");
        }
    });
}

// ------------------------------

function onLikeButton(post_id) {
    // post_id = -1 when the post is in the post modal
    var post_modal = post_id == -1;
    if (post_modal)
        post_id = $("#modal-viewpost-postid").val();
    $.ajax({
        url: "/ajax/command/like-post/",
        type: "POST",
        data: {
            "post-id": post_id
        },
        dataType: "json",
        success: function (data) {
            if (post_modal) {
                var modal_like = $("#modal-viewpost-like");
                modal_like.toggleClass("like-true", data["liked"]);
                modal_like.toggleClass("like-false", !data["liked"]);
            }
            else {
                var like = $("#like-" + data["post-id"]);
                like.toggleClass("like-true", data["liked"]);
                like.toggleClass("like-false", !data["liked"]);
                var s_like_count = $("#like-count-" + data["post-id"]);
                var deltaL = data["liked"] ? 1 : -1;
                s_like_count.val(parseInt(s_like_count.val()) + deltaL);
                console.log("adding " + deltaL + " to like count " + data["post-id"])
            }
        },
        failure: function (data) {
            console.log("Unable to like post");
        }
    });
}

function onRepostButton(target_post_id) {
    // TODO: Same as new post, but have target set to the reposted post, also means adding the post being reposted to the new post modal.
    /*var post_modal = post_id == -1;
     if (post_modal)
     {
     post_id = $("#modal-viewpost-postid").val()
     }
     $.ajax({
     url: "/ajax/repost/",
     type: "POST",
     data: {"post_id": post_id},
     dataType: "json",
     success: function (data) {
     var repost = $("#repost-" + data["post_id"]);
     repost.toggleClass("repost-button-true", data["reposted"]);
     repost.toggleClass("repost-button-false", !data["reposted"]);
     if (post_modal)
     {
     var modal_repost = $("#modal-viewpost-repost");
     modal_repost.toggleClass("repost-button-true", data["reposted"]);
     modal_repost.toggleClass("repost-button-false", !data["reposted"]);
     }
     }
     });*/
}

function onReplyButton(target_username, parent_post_id) {
    $("#post-form textarea[name='body']").val("@" + target_username + " ");
    $("#post-form input[name='parent']").val(parent_post_id);
    $("#new-post-modal").modal();
}

function onFollowButton(target_username) {
    $.ajax({
        url: "/ajax/command/follow-user/",
        type: "POST",
        data: {
            "username": target_username
        },
        dataType: "json",
        success: function (data) {
            var follow = $("#follow-" + data["username"]);
            follow.toggleClass("follow-button-true", data["follow"]);
            follow.toggleClass("follow-button-false", !data["follow"]);
        },
        failure: function (data) {
            console.log("Unable to follow user");
        }
    });
}

function onPostTo(target_username) {
    if (target_username != null)
        $("#post-form textarea[name='body']").val("@" + target_username + " ");
    $("#post-form input[name='parent']").val("");
    $("#new-post-modal").modal();
}


function onReportUserButton(target_username) {
    // TODO: Needs modal to add report message before ajaxing it off.
    $.ajax({
        url: "/ajax/command/report-user/",
        type: "POST",
        data: {
            "username": target_username
        },
        dataType: "json",
        success: function (data) {
            // FIXME: Temp
            alert("TEMP: report received");
        },
        failure: function (data) {
            console.log("Unable to report user");
        }
    });
}

function onBlockButton(target_username) {
    // TODO: Should have a confirmation dialogue here
    $.ajax({
        url: "/ajax/command/block-user/",
        type: "POST",
        data: {
            "username": target_username
        },
        dataType: "json",
        success: function (data) {
            // FIXME: Temp
            alert("TEMP: user has been blocked");
        },
        failure: function (data) {
            console.log("Unable to block user");
        }
    });
}

function linkifyPostBody(postBody) {
    try {
        // replace hash tags
        postBody.innerHTML = postBody.innerHTML.replace(/(^|)#(\w+)/g,
            function (s) {
                return '<a href="/tag/' + s.replace(/#/, '') + '">' + s + '</a>';
            });
    }
    catch (err) {
    }

    try {
        // replace mentions
        var mentions = [];
        postBody.innerHTML = postBody.innerHTML.replace(/(^|)@(\w+)/g,
            function (s) {
                var username = s.replace(/@/, '');
                var id = guid();
                mentions.push({
                    "username": username,
                    "link_id": id
                });
                return '<a id="' + id + '" href="/user/' + username + '">' + s + '</a>';
            });
        // register hover cards
        for (var i = 0; i < mentions.length; i++)
            registerHoverCard('#' + mentions[i].link_id, mentions[i].username);
    }
    catch (err) {
    }
}

// Writes a tag to the trending panel
function writeTrend(tag) {
    var div_parent = $("#trend-tags");
    var a_trend = document.createElement("a");
    div_parent.append(a_trend);
    a_trend.setAttribute("class", "body");
    a_trend.setAttribute("href", "/tag/" + tag);
    a_trend.appendChild(document.createTextNode(tag));
    div_parent.append(document.createElement("br"));
}

// Displays a profile card at the given position
function viewProfileCard(target_username, top, left) {
    $.ajax({
        url: "/ajax/get/user/",
        type: "POST",
        data: {
            "username": target_username
        },
        dataType: "json",
        success: function (data) {
            $("#profile-card-banner").attr("src", data["banner_url"]);
            $("#profile-card-profile-link").attr("href", "/user/" + target_username);
            $("#profile-card-avatar").attr("src", data["avatar_url"]);
            $("#profile-card-display-name").text(data["display_name"]);
            $("#profile-card-user-name").text(target_username);
            $("#profile-card-bio").text(data["bio"]);
            $("#profile-card-profile-link-posts").attr("href", "/user/" + target_username);
            $("#profile-card-profile-post-count").text(data["post_count"]);
            $("#profile-card-profile-link-following").attr("href", "/user/" + target_username + "/following");
            $("#profile-card-profile-following-count").text(data["following_count"]);
            $("#profile-card-profile-link-followers").attr("href", "/user/" + target_username + "/followers");
            $("#profile-card-profile-follower-count").text(data["follower_count"]);
            $("#global-profile-card").css({top: top, left: left}).show();
        },
        failure: function (data) {
            console.log("Unable to load user '" + target_username + "'")
        }
    });
}

// Causes a hover card to be displayed when mousing over the given element
function registerHoverCard(element_id, target_username) {
    var delay = 500;
    var timer;

    $(element_id).hover(function (event) {
        timer = setTimeout(function () {
            var left = cursorX - 30;
            var top = cursorY - 30;
            viewProfileCard(target_username, top, left);
        }, delay);
    }, function () {
        clearTimeout(timer);
    });viewPost
}

function formatTime(unixTime) {
    var longMonthNames = [
        "January", "February", "March",
        "April", "May", "June", "July",
        "August", "September", "October",
        "November", "December"
    ];

    var shortMonthNames = [
        "Jan", "Feb", "Mar",
        "Apr", "May", "Jun", "Jul",
        "Aug", "Sep", "Oct",
        "Nov", "Dec"
    ];
    var dateTime = new Date(unixTime * 1000);
    var amPm = dateTime.getHours() > 12 ? "pm" : "am";
    var hours = dateTime.getHours() > 12 ? dateTime.getHours() - 12 : dateTime.getHours();
    var mins = dateTime.getMinutes() < 10 ? "0" + dateTime.getMinutes() : dateTime.getMinutes();
    var dateTimeFormatted = hours + ":" + mins + amPm + " on " +
        dateTime.getDate() + " " + shortMonthNames[dateTime.getMonth()] + " " + dateTime.getFullYear();

    var millsAgo = Date.now() - (unixTime * 1000);
    var secsAgo = Math.floor(millsAgo / 1000);
    var minsAgo = Math.floor(millsAgo / 1000 / 60);
    var hoursAgo = Math.floor(millsAgo / 1000 / 60 / 60);
    var daysAgo = Math.floor(millsAgo / 1000 / 60 / 60 / 24);
    var timeDeltaFormatted = "";
    if (daysAgo == 1)
        timeDeltaFormatted = daysAgo + " day ago";
    else if (daysAgo > 1)
        timeDeltaFormatted = daysAgo + " days ago";
    else if (hoursAgo == 1)
        timeDeltaFormatted = hoursAgo + " hour ago";
    else if (hoursAgo > 1)
        timeDeltaFormatted = hoursAgo + " hours ago";
    else if (minsAgo == 1)
        timeDeltaFormatted = minsAgo + " minute ago";
    else if (minsAgo > 1)
        timeDeltaFormatted = minsAgo + " minutes ago";
    else if (secsAgo == 1)
        timeDeltaFormatted = secsAgo + " second ago";
    else if (secsAgo > 1 || secsAgo == 0)
        timeDeltaFormatted = secsAgo + " seconds ago";
    else
        timeDeltaFormatted = "error";
    return timeDeltaFormatted + " • " + dateTimeFormatted;
}

// Writes post with extra detail to the DOM at the given parent
function writePostDetailed(post_json, parent_selector) {

}

// Writes a post to the DOM at the given parent
function writePost(post_json, parent_selector) {
    function c_div(parent, _class, content) {
        var e = document.createElement("div");
        if (_class)
            e.setAttribute("class", _class);
        if (content)
            e.appendChild(document.createTextNode(content));
        parent.append(e);
        return e;
    }

    function c_span(parent, _class, content) {
        var e = document.createElement("span");
        if (_class)
            e.setAttribute("class", _class);
        if (content) {
            e.appendChild(document.createTextNode(content));
        }
        parent.append(e);
        return e;
    }

    // Default the parent selector to 'posts'
    if (parent_selector == null)
        parent_selector = "#posts";

    var userUrl = "/user/" + post_json["user"]["username"];

    var post_guid = post_json["id"];
    var d_post = c_div($(parent_selector), "post");
    d_post.setAttribute("id", post_guid);
    $(d_post).on('click', function(e) {
        if ($(e.target).hasClass("block-expand"))
            return;
        viewPost(post_guid);
    });

    var d_avatar = c_div(d_post, "avatar-container block-expand");
    d_avatar.setAttribute("onclick", userUrl);
    var i_avatar = document.createElement("img");
    d_avatar.append(i_avatar);
    i_avatar.setAttribute("src", post_json["user"]["avatar-url"]);
    i_avatar.setAttribute("class", "image block-expand");

    var s_displayname = c_span(d_post, "display-name block-expand", post_json["user"]["display-name"]);
    s_displayname.setAttribute("href", userUrl);

    var s_username = c_span(d_post, "username block-expand", post_json["user"]["username"]);
    s_username.setAttribute("href", userUrl);
    var s_time = c_span(d_post, "time", " • " + formatTime(post_json["time"]));

    var d_body = c_div(d_post, "body", post_json["body"]);

    var d_actions = c_div(d_post, "actions");

    var s_reply_container = c_span(d_actions, "action-container");
    var s_reply = c_span(s_reply_container, "action-button icon reply block-expand");
    s_reply.setAttribute("onclick",
        "onReplyButton('" + post_json["user"]["username"] + "', " + post_json["id"] + ")");
    var s_reply_count = c_span(s_reply_container, "action-count", post_json["reply-count"]);
    s_reply_count.setAttribute("id", "reply-count-" + post_json["id"]);

    var s_like_container = c_span(d_actions, "action-container");
    var like_class = "action-button icon like-false block-expand";
    if (post_json["liked"])
        like_class = "action-button icon like-true block-expand";
    var s_like = c_span(s_like_container, like_class);
    s_like.setAttribute("onclick", "onLikeButton(" + post_json["id"] + ")");
    s_like.setAttribute("id", "like-" + post_json["id"]);
    var s_like_count = c_span(s_like_container, "action-count", post_json["like-count"]);
    s_like_count.setAttribute("id", "like-count-" + post_json["id"]);

    var s_repost_container = c_span(d_actions, "action-container");
    var repost_class = "action-button icon repost-false block-expand";
    if (post_json["reposted"])
        repost_class = "action-button icon repost-true block-expand";
    var s_repost = c_span(s_repost_container, repost_class);
    var s_repost_count = c_span(s_repost_container, "action-count", post_json["repost-count"]);
    s_repost_count.setAttribute("id", "repost-count-" + post_json["id"]);
}

// Opens the post with the given id in the view post modal
function viewPost(post_id) {
    $.ajax({
        url: "/ajax/get/post/",
        type: "POST",
        data: {
            "post-id": post_id
        },
        dataType: "json",
        success: function (data) {
            $("#modal-viewpost-parent").empty();
            if (data["parent"])
                writePost(data["parent"], "#modal-viewpost-parent");
            var ta = $("#modal-viewpost-replybox-textarea");
            ta.val("");
            ta.attr("placeholder", "Reply to @" + data["main"]["user"]["username"]);
            var ta_on_focus =
                "$('#viewpost-reply-form textarea[name=\"body\"]').val('@" + data['main']['user']['username'] + " ');" +
                "$('#viewpost-reply-form textarea[name=\"body\"]').selectRange(50);";
            var ta_on_click =
                "var ta = $('#viewpost-reply-form textarea[name=\"body\"]');" +
                "if (ta.val() == '' || ta.val() == '@Tim ') " +
                "   ta.selectRange(50);";
            ta.attr("onfocus", ta_on_focus);
            ta.attr("onclick", ta_on_click);
            $("#modal-viewpost-replybox-parent").val(data["main"]["id"]);
            $("#modal-viewpost-replybox-target").val("");
            $("#modal-viewpost-main").empty();
            writePost(data["main"], "#modal-viewpost-main");
            $("#modal-viewpost-replies").empty();
            for (var i = 0; i < data["replies"].length; i++) {
                writePost(data["replies"][i], "#modal-viewpost-replies");
            }
            $("#modal-viewpost").modal();
        },
        failure: function (data) {
            console.log("Unable to load post '" + post_id + "'");
        }
    });
}

// Loads the current user's main feed
function loadMainFeed() {
    if (!post_time_oldest)
        post_time_oldest = INT_MAX;
    if (!post_time_newest)
        post_time_newest = 0;
    $.ajax({
        url: "/ajax/get/feed/",
        type: "POST",
        data: {
            "time-oldest": post_time_oldest
        },
        dataType: "json",
        success: function (data) {
            post_time_oldest = data["time-oldest"];
            post_time_newest = data["time-newest"];
            for (var i = 0; i < data["posts"].length; i++) {
                writePost(data["posts"][i]);
            }
        },
        failure: function (data) {
            console.log("Unable to load main feed");
        }
    });
}

// Updates the notification count
function updateNotificationCount() {
    $.ajax({
        url: "/ajax/get/unread-notif-count/",
        type: "POST",
        data: {},
        dataType: "json",
        success: function (data) {
            if (data["count"] != "0")
                $("#nav-notifications").text(data["count"]);
            else
                $("#nav-notifications").text("");        },
        failure: function (data) {
            console.log("Unable to load unread notification count");
        }
    });
}

// Updates the trending tags
function updateTrends() {
    $.ajax({
        url: "/ajax/get/trends/",
        type: "POST",
        data: {},
        dataType: "json",
        success: function (data) {
            $("#trend-tags").empty();
            for (var i = 0; i < data.length; i++)
                writeTrend(data[i]);
        },
        failure: function (data) {
            console.log("Unable to load trends");
        }
    });
}

// Check for new posts
function checkNewPosts() {
    if (!post_time_newest)
        post_time_newest = 0;
    $.ajax({
        url: "/ajax/get/new-post-count/",
        type: "POST",
        data: {
            "time-newest": post_time_newest
        },
        dataType: "json",
        success: function (data) {
            var view_new_posts = $("#view-new-posts");
            if (data["count"] != 0) {
                if (data["count"] == 1)
                    view_new_posts.text("View 1 new post");
                else
                    view_new_posts.text("View " + data["count"] + " new posts");
                document.title = "(" + data["count"] + ") Gab | Feed";
                view_new_posts.removeClass("hidden");
            }
            else {
                view_new_posts.addClass("hidden");
            }
        },
        failure: function (data) {
            console.log("Unable to load new post count");
        }
    });
}
