import * as React from 'react';
import { ClassificationStat } from '../types/output';


type Props = {
    stats : ClassificationStat
}

const Stats: React.FC<Props>  = ({stats}) => {
    return <div>
       <div>Общее количество объектов: <b>{stats?.media_count || 0}</b></div> 
       <div>Количество размеченных: <b>{stats?.vote_count||0}</b></div> 

       
       {stats?.by_category && <ul className="ul-list">
           <div style={{marginTop:"10px"}}>Сущности(классификации)</div> 
           {stats.by_category.map((s) => <li key={s.category}>{s.category}: <b>{s.count}</b></li>)}
       </ul>}
    </div>
}

export default Stats