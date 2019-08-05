<div style="width:40945px;display:block;clear:both;">

   %for ch, miss_list in rows.items():

       <div style="width:40945px;display:block;clear:both;">
       <div style="background:#ccc;
                   height:64px;
                   width:132px;
                   float:left;
                   line-height: 64px;
                   margin-right:3px;
                   margin-bottom:3px;">
       <b>{{ch}}</b></div>

       % for frame in miss_list:
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
               {{frame[0]}}<br>{{frame[1]}}
               </div>
       % end
       </div>
   % end
</div>
