% from datetime import datetime as dt
% import time

% name = 0
% start = 1
% end = 2
<div style="width:40945px;display:block;clear:both;">

   %for ch, gaps_list in rows.items():

       <div style="width:40945px;display:block;clear:both;">
       <div style="background:#ccc;
                   height:64px;
                   width:132px;
                   float:left;
                   line-height: 64px;
                   margin-right:3px;
                   margin-bottom:3px;">
       <b>{{ch}}</b></div>

       % for frame in gaps_list:
           % first_id, first_times, next_id, next_times = frame
           % f_start = str(dt.strptime(time.ctime(int(first_times[start]) / 1000), '%a %b %d %H:%M:%S %Y'))
           % f_end = str(dt.strptime(time.ctime(int(first_times[end]) / 1000), '%a %b %d %H:%M:%S %Y'))
           % n_start = str(dt.strptime(time.ctime(int(next_times[start]) / 1000), '%a %b %d %H:%M:%S %Y'))
           % n_end = str(dt.strptime(time.ctime(int(next_times[end]) / 1000), '%a %b %d %H:%M:%S %Y'))
               <div style="background:#ccc;
                           width:350px;
                           float:left;
                           margin-right:3px;
                           margin-bottom:3px;
                           white-space:nowrap;
                           overflow:hidden;
                           padding:5px;
                           text-overflow:ellipsis;">
               <b>{{first_times[name]}}</b> {{f_start}}-{{f_end.split(' ')[1]}}<br><i>{{first_id}}</i>
               <br><b>{{next_times[name]}}</b> {{n_start}}-{{n_end.split(' ')[1]}}<br><i>{{next_id}}</i><br>
               </div>
       % end
       </div>
   % end
</div>
