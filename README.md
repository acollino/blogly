# Blogly
A model of a blog site, with relational databases for users, posts, and tags.

## Usage
Content on the site can be added via users, posts, and tags:
- Users have names, profile pictures, and lists of their posts.
- Posts display titles, text-based content, and lists of their tags.
- Tags only have names, but a tag can display all posts using it.

Each type of content can be edited and/or deleted as well.

Information is stored in a server-side relational database using PostgreSQL. Users and posts have a one-to-many relationship, while posts and tags have a many-to-many relationship, implemented using a junctional table.

The app is hosted on Heroku and is accessible at https://acollino-blogly.herokuapp.com.

## Previews
<img src="https://user-images.githubusercontent.com/8853721/180053359-74127e60-fe30-4646-9734-d392acaa71f8.png" alt="Blogly home page" style="width: 700px">

<img src="https://user-images.githubusercontent.com/8853721/180053414-011db591-e8c4-4013-965f-da962b4e0da8.png" alt="Blogly user-details page" style="width: 500px"><img src="https://user-images.githubusercontent.com/8853721/180053471-65fe64d7-0a50-4fbe-9cde-517e5dd8066d.png" alt="Blogly page for submitting a new post" style="width: 500px">
<img src="https://user-images.githubusercontent.com/8853721/180053573-b71e7f71-f5b2-4026-a499-982786dd650c.png" alt="Blogly page for editing a user" style="width: 500px">


## Attributions
[Edit, Delete, Home symbols](https://fonts.google.com/icons)
