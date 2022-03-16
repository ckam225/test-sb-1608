

export interface Image {
    id: number;
    name: string;
    category: string;
    url: string;
    created_at: Date;
    updated_at: Date;
}

export interface User {
    id: number;
    name: string;
    username: string;
    on_bot: boolean;
    created_at: Date;
    access_token: string;
    token_type: string;
    token_expire_at: Date;
}


export interface ByCategory {
    category: string;
    count: number;
}

export interface ClassificationStat {
    media_count?: number;
    vote_count?: number;
    by_category: ByCategory[];
}