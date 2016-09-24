$(function() {

  function filterByTag(tag) {
    var target = 'tag-' + tag;
    var posts = $(".tags-posts > .post-list > li");
    posts.css('display', 'block');
    posts.filter(":not(." + target + ")")
      .css('display', 'none');
    $('.tags-list').css('display', 'none');
    $('.tags-posts').css('display', 'block');
    var title = `Posts of Tag <${tag}>`;
    $('.post-title').text(title);
    document.title = title;
  }

  if (location.search.length) {
    var tags = $(location.search.substring(1).split('&'))
      .filter(function (i, e) {
        return e.startsWith('tag=');
      }).map(function (i, e) {
        return e.split('=')[1];
      });
    if (tags.length) {
      filterByTag(tags[0]);
    }
  }

  var taglinks = $(".tags-posts > .post-list > li .post-tags > a");
  taglinks.attr('href', null);
  taglinks.click(function (e) {
    filterByTag(e.target.text);
  })
})
