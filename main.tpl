% from datetime import datetime as dt
% from datetime import timedelta

<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
 <title>EPG DATA</title>
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
   position: relative;
   z-index: 1;
  }
  #boxa {
   position: absolute;
   top: 15px;
   left: 30px;
   z-index: 10;
  }

 </style>

 <body>
    <form action="/" method="post">
    <select size="1" name="date">
       <option value={{today.strftime("%Y%m%d")}}>{{today.strftime("%Y-%m-%d")}}</option>
         % for day in dates[::-1]:
             <option value={{day.strftime("%Y%m%d")}}>{{day.strftime("%Y-%m-%d")}}</option>
         % end
    </select>

    <select size=1 name="type">
       <option value="line">Line</option>
       <option value="gap">Gap</option>
       <option value="overlap">Overlap</option>
       <option value="missing">Missing Data</option>
    </select>

    <select size=1 name="country">
       <option value="NL">NL</option>
       <option value="AT">AT</option>
       <option value="CH">CH</option>
       <option value="CZ">CZ</option>
       <option value="HU">HU</option>
       <option value="PL">PL</option>
       <option value="RO">RO</option>
       <option value="SK">SK</option>
    </select>

      <input value="*Show me what U got*" type="submit">
    </form>

   <div id="box"><div id="boxa"></div>
   <div style="width: 40945px; display: block; clear: both;">
   <div style="background: #ccc; width: 132px; float: left; margin-right: 3px; margin-bottom: 3px;">&nbsp;</div>
   <div style="background: #ccc; width: 5760px; float: left; margin-right: 10px; margin-bottom: 3px;">
   <b>&nbsp;{{date}}</b>
   <!---
       % for i in range(24):
           % offset = (i * 240)+135
           <div class="vertical-line" id="verticalline" style="left: {{offset}}px; height: 700px;"></div>
       % end
       --->
   </div></div>
</body>
