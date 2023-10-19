# Project Title: COUPLE
#### Video Demo:  <URL https://youtu.be/n6lUG9m5zbs>
#### Description:
概要：
    私がファイナルプロジェクトで作ったものは、COUPLEという、カップル向けのウェブサイトです。
    このサイトではカップルが二人のの思い出を、写真とコメントで残しておくことが出来ます。
    また付き合った日を登録することで、付き合ってから何日経過したかをすぐに確認することが出来ます。
    これにより一緒にいる時間の長さを感じることが出来、お互いの大切さを再認識することを目的としました。


各ファイルの説明：

static/uploads:　
    ユーザーがサイト内で登録、また投稿した画像を保存します。（※画像ファイルの拡張子には制限があります。）

static/favicon.ico:
    サイトのアイコンのファイルです。カップル用ということでハートのアイコンにしました。

static/styles.css:
    cssファイルです。カップル用にかわいいデザイン色を心がけました。

templates/index.html:
    サイトのホーム画面のHTMLファイルです。
    登録した日にちと現在の時間から、付き合ってから経った日数を計算した結果を表示します。
    真ん中に彼氏、彼女それぞれの写真を登録するための丸い枠があります。間に♡を置きラブラブ感を演出しました。
    一番下には画像を登録するフォームがあります。見た目をよくするために選択したファイルの名前などは表示されないように工夫しました。
    フォームのアイコンは男性、女性それぞれの絵文字とすることで分かりやすくしました。

templates/apology.html:
    ユーザーがサポートされていない動作を実行しようとした際に表示されるページのHTMLファイルです。

templates/layout.html:
    すべてのページに共通するレイアウトをかいたHTMLファイルです。
    カップル用に背景をピンクにしました。

templates/login.html:
    ログインのためのページのHTMLファイルです。

templates/password.html:
    パスワードを変更するためのページのHTMLファイルです。

templates/post.html:
    投稿のためのHTMLファイルです。
    画像とコメントを投稿することが出来ます。（画像の添付は必須です。）

templates/posted.html:
    投稿が正しく行われた際に表示するページのHTMLファイルです。

templates/register.html:
    ユーザーの登録を行います。
    ユーザーID、パスワード、付き合った日を登録します。
    他のユーザーと同じIDは登録が出来ないようになっています。

templates/story.html:
    投稿した写真とコメントを表示するHTMLファイルです。
    同時に投稿した日にちを下に表示するようになっています。

app.py:
    pythonで書かれたファイルです。このファイルでサイトのコントロールを行っています。

    19-22行では画像を保存する場所を指定しています。また使うことのできる拡張子を'png', 'jpg', 'gif', 'JPG',
    の4つとしました。

    34-39行で投稿した写真のURLを保存するpostsテーブル,
    ホーム画面に表示する写真を保存するpicturesテーブル,
    付き合い始めた日を保存するdatesテーブルを作成しました。
    すべてのテーブルでuser_id, idを利用して間をつないでいます。
    またこの動作はテーブルが存在していないときにのみ行われることになっています。

    以下には各HTMLファイルを動かすコードが書いてあります。

    56-106行：index.html
    POSTで通信が行われた時、id=boy,girlであるファイルを取得します。
    どちらかのファイルがNULLの時エラーを返します。
    boy,girlのファイルが存在し、拡張子が適切なものであるとき、このファイルを保存します。
    その後このファイル名をpicturesテーブルに挿入し、リダイレクトを実行します。
    またpicturesテーブルに保存されている最新の写真のURLを取得し、
    付き合った日から現在までの日数を計算し、index.htmlに送信します。

    109－136行：post.html
    postのとき、投稿ページで選択された写真のファイル名とテキストを取得して、
    今日の日にちとともにpostsテーブルに挿入します。

    140-173行：login.html
    ユーザーネーム、パスワードが入力されていることを確認し、入力したパスワードからhashを取得し、
    usersテーブルに保存します。

helper.py:
    app.pyで使う関数が書いてあるpythonファイルです。
    関数をこちらに書くことでapp.pyファイルの煩雑さを軽減しました。

couple.db:
    登録した写真や、日付、パスワードなどを保存するデータベースです。

-----------------------------------------------------------------------------------

Overview.
    My final project is a website for couples called COUPLE.
    This website allows couples to keep their memories together with photos and comments.
    By registering the date they started dating, couples can immediately see how many days have passed since they started dating.
    This allows couples to feel the length of time they have been together and to reaffirm the importance of their relationship.


Description of each file

static/uploads:　
    Stores images that users have registered or posted on the site. (*Image file extensions are restricted.)

static/favicon.ico:
    This is the file for the site's icons. We chose the heart icon because it is for couples.

static/styles.css:
    This is a css file. I tried to create a cute design for couples.

templates/index.html:
    HTML file of the home page of the site.
    It displays the result of calculating the number of days since they started dating based on the registered date and the current time.
    There is a round frame in the middle for registering pictures of both boyfriend and girlfriend. A ♡ is placed between them to create a sense of love.
    At the bottom, there is a form to register images. To improve the appearance, the name of the selected file is not displayed.
    The icons on the form are pictorial symbols of male and female.

templates/apology.html:
    HTML file of the page that is displayed when a user tries to perform an unsupported action.

templates/layout.html:
    HTML file with the layout common to all pages.
    The background color is pink for couples.

templates/login.html:
    HTML file for the login page.

templates/password.html:
    HTML file of the page to change the password.

templates/post.html:
    HTML file for posting.
    You can post images and comments. (Attaching images is mandatory.)

templates/posted.html:
    HTML file for the page that is displayed when a post is successfully made.

templates/register.html:
    This is used to register users.
    Register user ID, password, and date of dating.
    The same ID as other users cannot be registered.

templates/story.html:
    HTML file to display posted photos and comments.
    The date of posting is displayed at the bottom of the file.

app.py:
    A file written in python. This file controls the site.

    Lines 19-22 specify where the images are stored. The file extension is 'png', 'jpg', 'gif', 'JPG',
    The following four are used.

    The posts table to store the URLs of the photos posted in lines 34-39,
    pictures table to store pictures to be displayed on the home screen,
    We created a dates table to store the date we started dating.
    All tables are connected using user_id and id.
    This behavior is only supposed to be done when the table does not exist.

    Below is the code that runs each HTML file.

    Lines 56-106: index.html
    When communication is made by POST, the file with id=boy,girl is retrieved.
    Returns an error if either file is NULL.
    If the file boy,girl exists and has the proper extension, this file is saved.
    It then inserts this file name into the pictures table and performs a redirect.
    It also retrieves the URL of the most recent photo stored in thepictures table and returns
    The number of days from the date of relationship to the present is calculated and sent to index.html.

    Lines 109-136: post.html
    When post, retrieve the file name and text of the photo selected on the post page, and
    Insert into the posts table with today's date.

    Lines 140-173: login.html
    Make sure you have entered your username and password, get the hash from the password you entered, and enter it in the
    Store in the users table.

helper.py:
    This is a python file containing the functions used in app.py.
    By writing functions in this file, the complexity of the app.py file is reduced.

couple.db:
    A database that stores registered photos, dates, passwords, etc.

Translated with www.DeepL.com/Translator (free version)

