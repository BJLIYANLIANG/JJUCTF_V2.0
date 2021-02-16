$(function () {
      var urlinfo = window.location.search.substring(1);
      var b = urlinfo.split('=');
      if(b[0]=='message'){
          var c = b[1];
          alert(decodeURI(c));
          //防止意外弹框
          window.location.href=window.location.pathname;
      };
    });