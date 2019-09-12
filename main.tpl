% from datetime import datetime as dt
% from datetime import date, timedelta

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
 <title>EPG Tracker</title>
 <style>
  body {
   font-size:12px;
   font-family:Arial, Verdana, sans-serif;
   }
  td {
   background:white;
   }
  .not-active {
   pointer-events: none;
   cursor: default;
   text-decoration: none;
   color: black;
   }
  div.vertical-line{
   width: 1px;
   background-color: #ddd;
   position: absolute;
   top: 0;
   left: 0;
   }
  div.time{
   background: #ccc;
   position: relative;
   padding-left: 0px;
   top: 0;
  }
  #box {
   position: absolute;
   top: 65px;
   z-index: 1;
  }
  #boxa {
   position: absolute;
   top: 85px;
  }

    .tabs {
        width: 100%;
        height: 50px;
    }
    .tabs ul,
    .tabs li {
        margin: 0;
        padding: 0;
        list-style: none;
    }
    .tabs,
    .tabs input[type="radio"]:checked + label {
        position: relative;
    }
    .tabs li,
    .tabs input[type="radio"] + label {
        display: inline-block;
    }
    .tabs li > div,
    .tabs input[type="radio"] {
        position: absolute;
    }
    .tabs li > div,
    .tabs input[type="radio"] + label {
        border: solid 1px #ccc;
    }
    .tabs {
    font: normal 11px Arial, Sans-serif;
        color: #404040;
    }
    .tabs li {
        vertical-align: top;
    }
    .tabs li:first-child {
        margin-left: 8px;
    }
    .tabs li > div {
        top: 18px;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 8px;
        overflow: auto;
        background: #fff;
        -moz-box-sizing: border-box;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
    }
    .tabs input[type="radio"] + label {
        margin: 0 8px 0 0;
        padding: 0 8px;
        line-height: 17px;
        background: #f1f1f1;
        text-align: center;
        border-radius: 5px 5px 0 0;
        cursor: pointer;
        -moz-user-select: none;
        -webkit-user-select: none;
        user-select: none;
    }
    .tabs input[type="radio"]:checked + label {
        z-index: 1;
        background: #fff;
        border-bottom-color: #fff;
        cursor: default;
    }
    .tabs input[type="radio"] {
        opacity: 0;
    }
    .tabs input[type="radio"] ~ div {
        display: none;
    }
    .tabs input[type="radio"]:checked:not(:disabled) ~ div {
        display: block;
    }
    .tabs input[type="radio"]:disabled + label {
        opacity: .5;
        cursor: no-drop;
    }

 </style>

 <body>
    <div class="tabs" style="position: fixed; z-index: 1">
      <ul>
        <li>
         <input type="radio" name="tabs-0" id="tabs-0-0" disabled="disabled"/>
            <label for="tabs-0-0">Prod</label>
         <div>
            % for acr in available:
                <a href="/{{'prod-' + acr}}">{{acr}}</a>
            % end

        </div>
       </li>
       <li>
         <input type="radio" name="tabs-0" checked="checked" id="tabs-0-1" />
           <label for="tabs-0-1">PreProd</label>
         <div>
            % for acr in available:
                <a href="/{{'preprod-' + acr}}">{{acr}}</a>
            % end
        </div>
        </li>
        <li>
          <input type="radio" name="tabs-0" id="tabs-0-2" disabled="disabled" />
            <label for="tabs-0-2">Pepper</label>
          <div>
          </div>
       </li>
       <li>
         <input type="radio" name="tabs-0" id="tabs-0-3" disabled="disabled" />
            <label for="tabs-0-3">Salt</label>
         <div>
         </div>
       </li>
      </ul>
    </div>

   % today = date.today()
   % yesterday = date.today() - timedelta(days=1)
   % two_days_ago_date = date.today() - timedelta(days=2)

   <div id="box">

   <div style="width: 18000px; display: block; clear: both;">
   <div style="background: #ccc; width: 132px; float: left; margin-right: 3px; margin-bottom: 3px;">&nbsp;</div>

   % for day in (two_days_ago_date, yesterday, today):
       <div style="background: #ccc; width: 5760px; float: left; margin-right: 0px; margin-bottom: 3px;">
       <b>&nbsp; {{day.strftime('%m/%d/%Y')}}</b>
       </div>
   % end


   </div></div>

   <div id="boxa">
</body>
