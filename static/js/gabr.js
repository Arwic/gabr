var global_profile_card;
var global_view_post;
var cursorX;
var cursorY;
var post_time_newest;
var post_time_oldest;

const INT_MAX = 2147483647;

$.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") }
});

$(document).ready(function () {
    global_view_post = $("#modal-viewpost");
    global_profile_card = $("#global-profile-card");

    $(document).mousemove(function(event){
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

    loadNotificationCount();
    loadTrends();
});

function guid() {
    var d = new Date().getTime();
    var id = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=="x" ? r : (r&0x3|0x8)).toString(16);
    });
    return id;
};


function getCookie(cookieName)
{
    if (document.cookie.length > 0)
    {
        var c_start = document.cookie.indexOf(cookieName + "=");
        if (c_start != -1)
        {
            c_start = c_start + cookieName.length + 1;
            var c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function onLikeButton(post_id)
{
    var post_modal = post_id == -1;
    if (post_modal)
    {
        post_id = $("#modal-viewpost-postid").val()
    }
    $.ajax({
        url: "/ajax/like/",
        type: "POST",
        data: {"post_id": post_id},
        dataType: "json",
        success: function (data) {
            var like = $("#like-" + data["post_id"]);
            like.toggleClass("like-button-true", data["liked"]);
            like.toggleClass("like-button-false", !data["liked"]);
            if (post_modal)
            {
                var modal_like = $("#modal-viewpost-like");
                modal_like.toggleClass("like-button-true", data["liked"]);
                modal_like.toggleClass("like-button-false", !data["liked"]);
            }
        }
    });
};

function onRepostButton(post_id)
{
    var post_modal = post_id == -1;
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
    });
}

function onFollowButton(target_username)
{
    $.ajax({
        url: "/ajax/follow/",
        type: "POST",
        data: {"user_name": target_username},
        dataType: "json",
        success: function (data) {
            var follow = $("#follow-" + data["user_name"]);
            follow.toggleClass("follow-button-true", data["follow"]);
            follow.toggleClass("follow-button-false", !data["follow"]);
        }
    });
}

function postTo(user)
{
    if (user != null)
        $("#id_post_body").children().first().val("@" + user + " ");
    $("#new-post-modal").modal();
}

function viewProfileCard(user_name, top, left)
{
    $.ajax({
        url: "/ajax/user/",
        type: "POST",
        data: {
            "user_name": user_name
        },
        dataType: "json",
        success: function (data) {
            $("#profile-card-banner").attr("src", data["banner_url"]);
            $("#profile-card-profile-link").attr("href", "/user/" + user_name);
            $("#profile-card-avatar").attr("src", data["avatar_url"]);
            $("#profile-card-display-name").text(data["display_name"]);
            $("#profile-card-user-name").text(user_name);
            $("#profile-card-bio").text(data["bio"]);
            $("#profile-card-profile-link-posts").attr("href", "/user/" + user_name);
            $("#profile-card-profile-post-count").text(data["post_count"]);
            $("#profile-card-profile-link-following").attr("href", "/user/" + user_name + "/following");
            $("#profile-card-profile-following-count").text(data["following_count"]);
            $("#profile-card-profile-link-followers").attr("href", "/user/" + user_name + "/followers");
            $("#profile-card-profile-follower-count").text(data["follower_count"]);

            $("#global-profile-card").css({top: top, left: left}).show();
        }
    });
}

function registerHoverCard(element_id, user_name)
{
    var delay = 500;
    var timer;

    $(element_id).hover(function(event) {
        timer = setTimeout(function() {
            var left = cursorX - 30;
            var top = cursorY - 30;
            viewProfileCard(user_name, top, left);
        }, delay);
    }, function () {
        clearTimeout(timer);
    });
}
function linkifyPostBody(postBody)
{
    try {
        // replace hash tags
        postBody.innerHTML = postBody.innerHTML.replace(/(^|)#(\w+)/g,
            function (s) {
                return '<a href="/tag/' + s.replace(/#/,'') + '">' + s + '</a>';
            });
    }
    catch (err) {}

    try {
        // replace mentions
        var mentions = [];
        postBody.innerHTML = postBody.innerHTML.replace(/(^|)@(\w+)/g,
            function (s) {
                var username = s.replace(/@/,'');
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
    catch (err) {}
}

function viewPost(post_id)
{
    $.ajax({
        url: "/ajax/post/",
        type: "POST",
        data: {
            "post_id": post_id
        },
        dataType: "json",
        success: function (data) {
            $("#modal-viewpost-postid").val(post_id);

            $("#modal-viewpost-postuser-avatar").attr("src", data["avatar_url"]);
            $("#modal-viewpost-postuser-link").attr("href", "/user/" + data["user_name"]);
            $("#modal-viewpost-postuser-displayname").text(data["display_name"]);
            $("#modal-viewpost-postuser-username").text(data["user_name"]);
            $("#modal-viewpost-post-time").text(data["time"]);
            var p_body = $("#modal-viewpost-post-body");
            p_body.text(data["body"]);
            linkifyPostBody(p_body[0]);
            $("#modal-viewpost-username").val(data["user_name"]);

            var modal_like = $("#modal-viewpost-like");
            modal_like.toggleClass("like-button-true", data["has_liked"]);
            modal_like.toggleClass("like-button-false", !data["has_liked"]);

            var modal_repost = $("#modal-viewpost-repost");
            modal_repost.toggleClass("repost-button-true", data["has_reposted"]);
            modal_repost.toggleClass("repost-button-false", !data["has_reposted"]);

            for (reply in data["replies"]) {
                alert("reply from " + reply["user_name"])
            }

            $("#modal-viewpost").modal();
        }
    });
}

function report(target_user_name)
{
    $.ajax({
        url: "/ajax/report-user/",
        type: "POST",
        data: {
            "target": target_user_name
        },
        dataType: "json",
        success: function (data) {
            console.log("Successfully reported " + target_user_name)
        },
        error: function () {
            console.log("Failed to report " + target_user_name)
        }
    });
}

function block(target_user_name)
{
    $.ajax({
        url: "/ajax/block-user/",
        type: "POST",
        data: {
            "target": target_user_name
        },
        dataType: "json",
        success: function (data) {
            console.log("Successfully blocked " + target_user_name)
        },
        error: function () {
            console.log("Failed to block " + target_user_name)
        }
    });
}

function writePost(post_json)
{
    // Parent div
    var div_parent = $("#posts");
    // Row
    var div_row = document.createElement("div");
    div_parent.append(div_row);
    div_row.setAttribute("class", "row");
    // Post block
    var div_post = document.createElement("div");
    div_row.appendChild(div_post);
    div_post.setAttribute("class", "b-post");
    // Repost text
    if (post_json["repost"]) {
        var repost_guid = guid();
        // Repost link
        var a_repost_link = document.createElement("a");
        div_post.appendChild(a_repost_link);
        a_repost_link.setAttribute("id", repost_guid);
        a_repost_link.setAttribute("href", "/user/" + post_json["repost-user"]["username"]);
        // Repost icon
        var span_repost_icon = document.createElement("span");
        a_repost_link.appendChild(span_repost_icon);
        span_repost_icon.setAttribute("class", "icon icon-repost");
        // Repost display name
        var span_repost_displayname = document.createElement("span");
        a_repost_link.appendChild(span_repost_displayname);
        span_repost_displayname.setAttribute("class", "repost-display-name");
        span_repost_displayname.appendChild(document.createTextNode(post_json["repost-user"]["displayname"] + " Reposted"));
        a_repost_link.appendChild(document.createElement("br"));
        registerHoverCard("#" + repost_guid, post_json["repost-user"]["username"]);
    }
    var post_guid = guid();
    // Post user link
    var a_link = document.createElement("a");
    div_post.appendChild(a_link);
    a_link.setAttribute("id", post_guid);
    a_link.setAttribute("href", "/user/" + post_json["post-user"]["username"]);
    // Post user avatar
    var div_avatar = document.createElement("div");
    a_link.appendChild(div_avatar);
    div_avatar.setAttribute("class", "avatar");
    var img_avatar = document.createElement("img");
    div_avatar.appendChild(img_avatar);
    img_avatar.setAttribute("class", "image");
    img_avatar.setAttribute("src", post_json["post-user"]["avatar"]);
    // Post user display name
    var span_post_displayname = document.createElement("span");
    a_link.appendChild(span_post_displayname);
    span_post_displayname.setAttribute("class", "display-name");
    span_post_displayname.appendChild(document.createTextNode(post_json["post-user"]["displayname"]));
    registerHoverCard("#" + post_guid, post_json["post-user"]["username"]);
    // Post user username
    var span_username = document.createElement("span");
    div_post.appendChild(span_username);
    span_username.setAttribute("class", "username");
    span_username.appendChild(document.createTextNode(post_json["post-user"]["username"]));
    // Post time
    var span_time = document.createElement("span");
    div_post.appendChild(span_time);
    span_time.setAttribute("class", "time");
    span_time.appendChild(document.createTextNode(post_json["post"]["time"]));
    // Post body
    var p_body = document.createElement("p");
    div_post.appendChild(p_body);
    p_body.setAttribute("class", "body");
    p_body.appendChild(document.createTextNode(post_json["post"]["body"]));
    linkifyPostBody(p_body);

    var div_actions = document.createElement("div");
    div_post.appendChild(div_actions);
    div_actions.setAttribute("class", "post-action-button-container");

    // Like button
    var button_like = document.createElement("button");
    div_actions.appendChild(button_like);
    button_like.setAttribute("onclick", "onLikeButton(" + post_json["post"]["id"] + ")");
    button_like.setAttribute("class", "post-action-button");
    var span_like_icon = document.createElement("span");
    button_like.appendChild(span_like_icon);
    if (post_json["post"]["liked"])
        span_like_icon.setAttribute("class", "icon like-button-true");
    else
        span_like_icon.setAttribute("class", "icon like-button-false");
    span_like_icon.setAttribute("id", "like-" + post_json["post"]["id"]);
    // Repost button
    var button_repost = document.createElement("button");
    div_actions.appendChild(button_repost);
    button_repost.setAttribute("onclick", "onRepostButton(" + post_json["post"]["id"] + ")");
    button_repost.setAttribute("class", "post-action-button");
    var span_repost_icon = document.createElement("span");
    button_repost.appendChild(span_repost_icon);
    span_repost_icon.setAttribute("id", "repost-" + post_json["post"]["id"]);
    if (post_json["post"]["reposted"])
        span_repost_icon.setAttribute("class", "icon repost-button-true");
    else
        span_repost_icon    .setAttribute("class", "icon repost-button-false");
    // Expand button
    var button_expand = document.createElement("button");
    div_actions.appendChild(button_expand);
    button_expand.setAttribute("onclick", "viewPost(" + post_json["post"]["id"] + ")");
    button_expand.setAttribute("class", "post-action-button");
    var span_expand_icon = document.createElement("span");
    button_expand.appendChild(span_expand_icon);
    span_expand_icon.setAttribute("class", "icon icon-postdetail");
}

function loadPosts(type, count, target, oldest, newest)
{
    if (oldest == null)
        oldest = 0;
    if (newest == null)
        newest = INT_MAX;
    $.ajax({
        url: "/ajax/load-posts/",
        type: "POST",
        data: {
            "type": type,
            "count": count,
            "time-oldest": oldest,
            "time-newest": newest,
            "target": target
        },
        dataType: "json",
        success: function (data) {
            data = JSON.parse(data);
            post_time_oldest = data["time-oldest"];
            post_time_newest = data["time-newest"];
            data["posts"].forEach(function(obj) { writePost(obj); });
        },
        error: function () {
            console.log("Failed to load posts")
        }
    });
}

function loadNotificationCount()
{
    $.ajax({
        url: "/ajax/load-notification-count/",
        type: "POST",
        data: { },
        dataType: "json",
        success: function (data) {
            data = JSON.parse(data);
            if (data["count"] != "0")
                $("#nav-notifications").text(data["count"]);
        },
        error: function () {
            console.log("Failed to load notifications");
        }
    });
}

function writeTrend(tag)
{
    var div_parent = $("#trends");
    var a_trend = document.createElement("a");
    div_parent.append(a_trend);
    a_trend.setAttribute("class", "body");
    a_trend.setAttribute("href", "/tag/" + tag);
    a_trend.appendChild(document.createTextNode(tag));
    div_parent.append(document.createElement("br"));
}

function loadTrends()
{
    $.ajax({
        url: "/ajax/load-trends/",
        type: "POST",
        data: { },
        dataType: "json",
        success: function (data) {
            data = JSON.parse(data);
            data["trends"].forEach(function(obj) { writeTrend(obj); });
        },
        error: function () {
            console.log("Failed to load trends");
        }
    });
}

function checkNewPosts()
{
    $.ajax({
        url: "/ajax/check-posts/",
        type: "POST",
        data: {
            "time-oldest": post_time_newest,
            "time-newest": INT_MAX
        },
        dataType: "json",
        success: function (data) {
            if (data["count"] != 0) {
                var view_new_posts = $("#view-new-posts");
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
        error: function () {

        }
    });
}

function loadOlderPosts(type, target)
{
    loadPosts(type, 50, target, 0, post_time_oldest);
}