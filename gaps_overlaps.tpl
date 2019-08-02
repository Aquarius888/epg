    <table border=1>
   %for ch, gaps_list in rows.items():
       <tr bgcolor="#ddd"><th width="150px">{{ch}}</th>
       %for frame in gaps_list:
           %first_title, first_id, first_end, next_title, next_id, next_start = frame
               <td>{{first_title}} {{first_end}}<br><i>{{first_id}}</i>
               <br>{{next_title}} {{next_start}}<br><i>{{next_id}}</i></td>
       %end
     </tr>
   %end
   </table>
