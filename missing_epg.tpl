% from datetime import datetime as dt
% import time

<div style="width:40945px;display:block;clear:both;">

   %for ch, miss_list in rows.items():

       % ch_number, ch_title = ch.split('|')
           <div style="width:40945px;display:block;clear:both;">
           <div style="background:#ccc;
                   height:64px;
                   width:132px;
                   float:left;
                   line-height: 64px;
                   margin-right:3px;
                   margin-bottom:3px;" title="{{ch_number}}_{{ch_title}}">

           <b>{{ch_title}}</b></div>

       % for frame in miss_list:
           % start = str(dt.strptime(time.ctime(int(frame[0]) / 1000), '%a %b %d %H:%M:%S %Y'))
           % end = str(dt.strptime(time.ctime(int(frame[1]) / 1000), '%a %b %d %H:%M:%S %Y'))
               <div style="background:#ccc;
                           height:54px;
                           width:200px;
                           float:left;
                           line-height: 26px;
                           text-align: center;
                           margin-right:3px;
                           margin-bottom:3px;
                           white-space:nowrap;
                           overflow:hidden;
                           padding:5px;
                           text-overflow:ellipsis;">
               {{start}}<br>{{end}}
               </div>
       % end
       </div>
   % end
</div>
