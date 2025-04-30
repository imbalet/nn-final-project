package interfaces

type RedisRepository interface {
	AddTask(id string, link string) (bool, error)
	IsTaskInQueue(key, id string) (bool, error)
}
