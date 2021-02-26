# Social Network

Twitter-like social network website for _making_, _liking_ posts and _following_ users.

### Written with:

- HTML
- CSS (Bootstrap 4.5.3)
- JavaScript
- Python 3.9
- Django 3.0.2
- SQLite 3

### Readme Navigation

1. [All Posts](#1-all-posts)
2. [New Post](#2-new-post)
3. [Profile Page](#3-profile-page)
   - [Follow](#31-subheader)
4. [Following](#4-header)
5. [Edit Post](#5-edit-post)
6. [Pagination](#6-header)
7. ["Like" and "Unlike"](#7-like-and-unlike)
8. [Future improvements](#8-future-improvements)

[My contacts](#my-contacts)

## 1. All Posts:

On the front page **user** can see all **posts** from all **users** with the most recent posts coming first.

Also at any time **user** can click on _**All Posts**_ link in the navbar to be taken to front page with all **posts**.

![front page](/readmedia/all-posts.png)

## 2. New Post:

**Users** who are signed in can click on _**New Post**_ link in the navbar, write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

![creating a new post](/readmedia/new-post.gif)

## 3. Profile Page:

Clicking on a **username** will load that **user’s** profile page.
That page displays:

- Number of followers the **user** has
- Number of people that **user** follows
- All post made by that **user** in reverse chronological order

![alt text](/readmedia/profile-page.gif)

### 3.1 Follow/Unfollow:

For any other **user** who is signed in, page also displays a _**Follow**_ or _**Unfollow**_ button that let the current **user** toggle whether or not they are following this **user’s** posts.

![follow/unfollow user](/readmedia/follow.gif)

## 4. Following:

User can click on the _**Following**_ link in the navbar, doing so **user** will be taken to a page where they see all posts made by **users** that the current **user** follows.

![following](/readmedia/following.gif)

## 5. Edit Post:

Users can click an _**Edit**_ button on any of their own posts to edit that post.

![edit post](/readmedia/edit-post.gif)

## 6. Pagination:

On any page that displays posts can be only 10 of them.
If there are more than 10 posts, a _**Next**_ button appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a _**Previous**_ button appears to take the **user** to the previous page of posts as well.

![pagination](/readmedia/pagination.gif)

## 7. "Like" and "Unlike":

Users who signed in is able to click a _**like button**_ on any post to toggle whether or not they “like” that post.

![liking posts](/readmedia/liking.gif)

## 8. Future improvements:

1. Switch from bootstrap to css
2. Improve ui
3. Add reposts

## My contacts

[Telegram](https://t.me/vincvader)

[VK](https://vk.com/vincvader)

[E-Mail](mailto:vincvader@mail.ru)
