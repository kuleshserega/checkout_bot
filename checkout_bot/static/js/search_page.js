$(document).ready(function(){
  $('#searchbtn').on('click', function(e){
    e.preventDefault();
    var search_term = $('#id_search').val();
    var search_type = $('#search_type').val();
    var string_row_search_geo = (search_type == '2') ? '&search_geo=' + $('#search_geo').val() : '';
    $.ajax({
      url: '/run-search/?search=' + search_term + '&search_type=' + search_type + string_row_search_geo,
      method: 'GET',
      success: function(data){
        show_msg(data);
        $('#id_search').val('');
        $('#search_geo').val('');
        $('.messages').find('.alert').each(function(){
          var el = $(this);
          setTimeout(function(){
            el.fadeOut(500, function(){
             el.remove();
            });
          }, 4000);
        });
      }
    });
  });

  $('body').on('click', '#update-task', function(e){
    e.preventDefault();
    var task_nmb = $(this).attr('task-nmb');
    $.ajax({
      url: '/update-task/' + task_nmb + '/',
      method: 'GET',
      success: function(data){
        show_msg(data);
        $('.messages').find('.alert').each(function(){
          var el = $(this);
          setTimeout(function(){
            el.fadeOut(500, function(){
             el.remove();
            });
          }, 4000);
        });
      }
    });
  });

  var queryDict = {}
  location.search.substr(1).split("&").forEach(
    function(item){
      queryDict[item.split("=")[0]] = item.split("=")[1]
    }
  );
  if (queryDict["page"] != undefined){
    var page = queryDict['page'];
  } else {
    var page = 1;
  }

  setInterval(function(){
    $.ajax({
      url: '/get_companies_list/?page=' + page,
      method: 'GET',
      success: function(data){
        var html = [];
        html.push(thead_html);
        for (var i=0;i<data['content'].length;i++){
          html.push(get_row_html(data['content'][i]));
        }

        $('#allProjectsTable').html(html.join());
      }
    });
  }, 5000);

  var thead_html = '<thead>' +
    '<tr>' +
      '<th>ID</th>' +
      '<th>Search term</th>' +
      '<th>Company ID</th>' +
      '<th>Geo</th>' +
      '<th>Search type</th>' +
      '<th>Date</th>' +
      '<th>Status</th>' +
      '<th>Link to search details</th>' +
      '<th>Save to CSV</th>' +
    '</tr>' +
  '</thead>';

  var get_row_html = function(row){
    var search_term = '';
    if(row['search_term']){ search_term = row['search_term']; }

    var companyId = '';
    if(row['companyId']){ companyId = row['companyId']; }

    var search_geo = '';
    if(row['search_geo']){ search_geo = row['search_geo']; }

    var search_type = '';
    if(row['search_type']){ search_type = row['search_type']; }

    var update_search_button = '';
    if(row['status'] == 10){ update_search_button = '<a id="update-task" class="btn" task-nmb="' + row['id'] + '">Update</a>'; }

    var row_template_html = '<tr>' +
      '<td>' + row['id'] + '</td>' +
      '<td>' + search_term + '</td>' +
      '<td>' + companyId + '</td>' +
      '<td>' + search_geo + '</td>' +
      '<td>' + search_type + '</td>' +
      '<td>' + row['date_created'] + '</td>' +
      '<td><span title="' + row['status_text'] + '" class="center glyphicon ' + row['status_icon'] + '"></span>' + update_search_button + '</td>' +
      '<td><a title="Search details" target="_blank" class="center" href="' + row['search_details_url'] + '"><img width=25 src="/static/img/details.png" /></a></td>' +
      '<td><a title="Save to CSV" class="center" href="' + row['employees_to_csv'] + '"><img width=25 src="/static/img/save.png" /></a></td>' +
    '</tr>';

    return row_template_html;
  }

  var show_msg = function(data){
    msg_block = '<div class="alert alert-' + data['status'] + '">' +
      '<span>' + data['msg'] + '</span>' +
    '</div>';

    $('.messages').html(msg_block);
  }

  $('#search_type').on('change', function(){
    var val = $(this).val();
    if (val == '1'){
      $('#search_geo').hide();
    } else if (val == '2'){
      $('#search_geo').show();
    }
  });
});
