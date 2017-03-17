var global_profile_card;
var global_view_post;
var cursorX;
var cursorY;
var post_time_newest;
var post_time_oldest;

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
        console.log("mouse moved")
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

// --------------- NYI ajax code (functions like these dont work due as return is  but the code can be used later) ---------------

function ajaxFeedUserPosts(target_username) {
    $.ajax({
        url: "/ajax/feed/user-posts/",
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
        url: "/ajax/feed/user-followers/",
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
        url: "/ajax/feed/user-follows/",
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
        url: "/ajax/feed/user-likes/",
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

// --------------- Handlers ---------------

function onLikeButton(post_id) {
    // post_id = 1 when the post is in the post modal
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
            var like = $("#like-" + data["post_id"]);
            like.toggleClass("like-button-true", data["liked"]);
            like.toggleClass("like-button-false", !data["liked"]);
            if (post_modal) {
                var modal_like = $("#modal-viewpost-like");
                modal_like.toggleClass("like-button-true", data["liked"]);
                modal_like.toggleClass("like-button-false", !data["liked"]);
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

// --------------- Processing ---------------

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

// --------------- Output ---------------

// Writes a tag to the trending panel
function writeTrend(tag) {
    var div_parent = $("#trends");
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
            writePost(data, "#modal-viewpost-main");
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

// Writes a post to the DOM at the given parent
function writePost(post_json, parent_selector) {
    // Parent div
    if (parent_selector == null)
        parent_selector = "#posts";
    var div_parent = $(parent_selector);
    // Row
    var div_row = document.createElement("div");
    div_parent.append(div_row);
    div_row.setAttribute("class", "row");
    // Post block
    var div_post = document.createElement("div");
    div_row.appendChild(div_post);
    div_post.setAttribute("class", "b-post");
    var post_guid = guid();
    // Post user link
    var a_link = document.createElement("a");
    div_post.appendChild(a_link);
    a_link.setAttribute("id", post_guid);
    a_link.setAttribute("href", "/user/" + post_json["user"]["user-name"]);
    // Post user avatar
    var div_avatar = document.createElement("div");
    a_link.appendChild(div_avatar);
    div_avatar.setAttribute("class", "avatar");
    var img_avatar = document.createElement("img");
    div_avatar.appendChild(img_avatar);
    img_avatar.setAttribute("class", "image");
    img_avatar.setAttribute("src", post_json["user"]["avatar-url"]);
    // Post user display name
    var span_post_displayname = document.createElement("span");
    a_link.appendChild(span_post_displayname);
    span_post_displayname.setAttribute("class", "display-name");
    span_post_displayname.appendChild(document.createTextNode(post_json["user"]["display-name"]));
    registerHoverCard("#" + post_guid, post_json["user"]["user-name"]);
    // Post user username
    var span_username = document.createElement("span");
    div_post.appendChild(span_username);
    span_username.setAttribute("class", "user-name");
    span_username.appendChild(document.createTextNode(post_json["user"]["user-name"]));
    // Post time
    var span_time = document.createElement("span");
    div_post.appendChild(span_time);
    span_time.setAttribute("class", "time");
    span_time.appendChild(document.createTextNode(post_json["time"]));
    // Post body
    var p_body = document.createElement("p");
    div_post.appendChild(p_body);
    p_body.setAttribute("class", "body");
    p_body.appendChild(document.createTextNode(post_json["body"]));
    linkifyPostBody(p_body);
    var div_actions = document.createElement("div");
    div_post.appendChild(div_actions);
    div_actions.setAttribute("class", "post-action-button-container");
    // Reply button
    var button_reply = document.createElement("button");
    div_actions.appendChild(button_reply);
    button_reply.setAttribute("onclick",
        "$('#view-post-close').click(); onReplyButton('" + post_json["user"]["username"] + "', " + post_json["id"] + ")");
    button_reply.setAttribute("class", "post-action-button");
    var span_reply_icon = document.createElement("span");
    button_reply.appendChild(span_reply_icon);
    span_reply_icon.setAttribute("class", "icon icon-reply");
    // Like button
    var button_like = document.createElement("button");
    div_actions.appendChild(button_like);
    button_like.setAttribute("onclick", "onLikeButton(" + post_json["id"] + ")");
    button_like.setAttribute("class", "post-action-button");
    var span_like_icon = document.createElement("span");
    button_like.appendChild(span_like_icon);
    if (post_json["post"]["liked"])
        span_like_icon.setAttribute("class", "icon like-button-true");
    else
        span_like_icon.setAttribute("class", "icon like-button-false");
    span_like_icon.setAttribute("id", "like-" + post_json["id"]);
    // Repost button
    var button_repost = document.createElement("button");
    div_actions.appendChild(button_repost);
    button_repost.setAttribute("onclick", "onRepostButton(" + post_json["id"] + ")");
    button_repost.setAttribute("class", "post-action-button");
    var span_repost_icon = document.createElement("span");
    button_repost.appendChild(span_repost_icon);
    span_repost_icon.setAttribute("id", "repost-" + post_json["id"]);
    if (post_json["post"]["reposted"])
        span_repost_icon.setAttribute("class", "icon repost-button-true");
    else
        span_repost_icon.setAttribute("class", "icon repost-button-false");
    // Expand button
    var button_expand = document.createElement("button");
    div_actions.appendChild(button_expand);
    button_expand.setAttribute("onclick", "viewPost(" + post_json["id"] + ")");
    button_expand.setAttribute("class", "post-action-button");
    var span_expand_icon = document.createElement("span");
    button_expand.appendChild(span_expand_icon);
    span_expand_icon.setAttribute("class", "icon icon-postdetail");
}

// --------------- Fetch for data ---------------

// Loads the current user's main feed
function loadMainFeed() {
    $.ajax({
        url: "/ajax/feed/main/",
        type: "POST",
        data: {
            "time-oldest": post_time_oldest,
            "time-newest": post_time_newest
        },
        dataType: "json",
        success: function (data) {
            post_time_oldest = data["time-oldest"];
            post_time_newest = data["time-newest"];
            for (var post in data["posts"])
                writePost(post);
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
            $("#trends").empty();
            for (var trend in data["trends"])
                writeTrend(trend);
        },
        failure: function (data) {
            console.log("Unable to load trends");
        }
    });
}

// Check for new posts
function checkNewPosts() {
    $.ajax({
        url: "/ajax/get/new-post-count/",
        type: "POST",
        data: {},
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

// Loads older posts
function loadOlderPosts(type, target) {
    loadPosts(type, 50, target, 0, post_time_oldest);
    // FIXME: THIS WAS JUST PASTED IN LAST NIGHT
    $.ajax({
        url: "/ajax/feed/main/",
        type: "POST",
        data: {
            "time-oldest": post_time_oldest,
            "time-newest": post_time_newest
        },
        dataType: "json",
        success: function (data) {
            post_time_oldest = data["time-oldest"];
            post_time_newest = data["time-newest"];
            for (var post in data["posts"])
                writePost(post);
        },
        failure: function (data) {
            console.log("Unable to load main feed");
        }
    });
}
