$(function() {
    var total_tabs = 0;

    // initialize first tab
    total_tabs++;
    addtab(total_tabs);

    $("#addtab, #litab").click(function() {
        total_tabs++;
        $("#tabcontent p").hide();
        addtab(total_tabs);
        return false;
    });

    function addtab(count) {
        var closetab = '<a href="" id="close'+count+'" class="close">&times;</a>';
        $("#tabul").append('<li id="t'+count+'" class="ntabs">Tab '+count+'&nbsp;&nbsp;'+closetab+'</li>');
        $("#tabcontent").append('<p id="c'+count+'">Tab Content '+count+'</p>');

        $("#tabul li").removeClass("ctab");
        $("#t"+count).addClass("ctab");

        $("#t"+count).bind("click", function() {
            $("#tabul li").removeClass("ctab");
            $("#t"+count).addClass("ctab");
            $("#tabcontent p").hide();
            $("#c"+count).fadeIn('slow');
        });

        $("#close"+count).bind("click", function() {
            // activate the previous tab
            $("#tabul li").removeClass("ctab");
            $("#tabcontent p").hide();
            $(this).parent().prev().addClass("ctab");
            $("#c"+count).prev().fadeIn('slow');

            $(this).parent().remove();
            $("#c"+count).remove();
            return false;
        });
    }
});