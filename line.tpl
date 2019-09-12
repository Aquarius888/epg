% from datetime import datetime as dt
% import time

  <style>
   .channel {
    background: #ccc;
    height: 64px;
    width: 132px;
    float: left;
    border-radius: 50%;
    line-height: 64px;
    margin-right: 3px;
    margin-bottom: 3px;
    text-align: center;
   }
   .prog {
    background:#ccc;
    width:130px;
    float:left;
    margin-right:3px;
    margin-bottom:3px;
    white-space:nowrap;
    overflow:hidden;
    padding:5px 0px;
    text-overflow:ellipsis;
   }
  div.vertical-line{
   width: 1px;
   background-color: #ddd;
   position: absolute;
   top: 0;
   left: 0;
   }
  </style>



   % now = time.time()
   % today = time.gmtime(now)
   % seconds_in_day = 86400
   % date_format = '%Y/%m/%d %H:%M:%S'
   % str_format = '{}/{}/{} 00:00:00'
   % midnight_struct_time = time.strptime(str_format.format(today.tm_year, today.tm_mon, today.tm_mday), date_format)
   % midnight_in_seconds = time.mktime(midnight_struct_time)
   % begin = midnight_in_seconds-2*seconds_in_day

   % offset = (now - begin)/15 + 135
     <div class="vertical-line" id="verticalline" style="left: {{offset}}px; height: 1700px;"></div>

   % for ch, line_dct in rows:
       % if line_dct:
           % ch_color = '#ccc'
           % ch_number, ch_title = ch.split('|')
           <div style="width:18000px;display:block;clear:both;">
           % if '#ccc' not in list(line_dct.values())[0]:
               % ch_color = '#dfb'
           % end
           <div class="channel" title="{{ch_number}}_{{ch_title}}" style="background: {{ch_color}}">

           <b>{{ch_title}}</b></div>

       % for prog_id, times in line_dct.items():
           % title, start, end, replay = times

           % # width compute
           % st = start

           % if st < begin*1000:
               % st = begin*1000
           % end

           % delta = int(end) - int(st)
           % width = delta / 15000
           % if width < 0:
               % continue
           % end

           % # color of box
           % color = replay

           % start = time.ctime(int(start) / 1000)
           % end = time.ctime(int(end) / 1000)
           <div class="prog" style="width: {{width - 3}}px; background: {{color}};"
           title="
           {{ch_number}}_{{ch_title}}
           {{title}}
           {{prog_id}}
           {{start}}
           {{end}}">
               {{title}}<br><br>{{start.split()[3]}}<br>{{end.split()[3]}}
           </div>
       % end
     </div>
   % end

