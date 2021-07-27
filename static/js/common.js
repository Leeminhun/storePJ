
/*header, footer 입력 스크립트*/
      function includeHTML() {
                        var z, i, elmnt, file, xhttp;
                        /* Loop through a collection of all HTML elements: */
                        z = document.getElementsByTagName("*");
                        for (i = 0; i < z.length; i++) {
                                elmnt = z[i];
                                /*search for elements with a certain atrribute:*/
                                file = elmnt.getAttribute("w3-include-html");
                                if (file) {
                                        /* Make an HTTP request using the attribute value as the file name: */
                                        xhttp = new XMLHttpRequest();
                                        xhttp.onreadystatechange = function () {
                                                if (this.readyState == 4) {
                                                        if (this.status == 200) { elmnt.innerHTML = this.responseText; }
                                                        if (this.status == 404) { elmnt.innerHTML = "Page not found."; }
                                                        /* Remove the attribute, and call this function once more: */
                                                        elmnt.removeAttribute("w3-include-html");
                                                        includeHTML();
                                                }
                                        }
                                        xhttp.open("GET", file, true);
                                        xhttp.send();
                                        /* Exit the function: */
                                        return;
                                }
                        }
                }

/*tab_Menu*/
$(document).ready(function (){


$('.big_tab li').first().addClass("activeClass");
  $(".tab-contents").not(':first').hide();

    $('.big_tab li').on('click',function(){
      $(this).addClass("activeClass").siblings().removeClass("activeClass");
      var link = $(this).find("a").attr("href");
      var link_num = link.substr(link.length-1);
      $("select#tabmenu option").eq(link_num-1).prop("selected", "selected");
      $(".tab-contents").hide();
      $(link).show();
    });

    $("select#tabmenu").on("change",function(){
      var select_link = $("select#tabmenu").val();
      var select_num = $(this).prop('selectedIndex');
      $('.big_tab li').eq(select_num).addClass("activeClass").siblings().removeClass('activeClass');
      $(".tab-contents").hide();
      $(select_link).show();
      console.log(select_link);
    });

})