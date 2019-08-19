% from datetime import datetime as dt
% import time

<div style="width:40945px;display:block;clear:both;">
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
    padding:5px;
    text-overflow:ellipsis;
   }
  </style>
   % for ch, line_dct in rows:
       % if line_dct:
           <div style="width:40945px;display:block;clear:both;">
           <div class="channel">
           <b>{{ch}}</b></div>
       % for prog_id, times in line_dct.items():
           % title, start, end = times

           % # width compute
           % st = start
           % if st < date*1000:
               % st = date*1000
           % end
           % delta = int(end) - int(st)
           % width = delta / 15000
           % if width == 0:
               % continue
           % end

           % start = str(dt.strptime(time.ctime(int(start) / 1000), '%a %b %d %H:%M:%S %Y'))
           % end = str(dt.strptime(time.ctime(int(end) / 1000), '%a %b %d %H:%M:%S %Y'))
           <div class="prog" style="width: {{width - 3}}px;"
           title="
           {{title}}
           {{start}}
           {{end}}">
               {{title}}<br><br>{{start.split()[1]}}<br>{{end.split()[1]}}
           </div>
       % end
     </div>
   % end
</div>
