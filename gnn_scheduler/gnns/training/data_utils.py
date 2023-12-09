from sklearn.model_selection import train_test_split

from gnn_scheduler.jssp import (
    JobShopInstance,
    load_pickle_instances_from_folders,
    load_metadata,
)


def train_test_split_by_name(
    instances: list[JobShopInstance], contains: list[str]
) -> tuple[list[JobShopInstance], list[JobShopInstance]]:
    """Splits the instances into train and test instances by name.

    If the instance name is contained in any of the strings in contains, it is
    considered a test instance. Otherwise, it is considered a train instance.

    Args:
        instances (list[JobShopInstance]): the instances to filter
        contains (list[str]): the strings to check if they are contained in the
            instance name

    Returns:
        tuple[list[JobShopInstance], list[JobShopInstance]]: the train and test
            instances
    """
    train_instances = []
    test_instances = []

    for instance in instances:
        is_train = True
        for string in contains:
            if string in instance.name:
                is_train = False
                break

        if is_train:
            train_instances.append(instance)
        else:
            test_instances.append(instance)

    return train_instances, test_instances


def get_names_with_n_machines(n_machines: int = 10, **kwargs) -> list[str]:
    """Returns the names of the instances with n_machines machines.

    Args:
        n_machines (int): the number of machines
        **kwargs: keyword arguments to pass to load_metadata

    Returns:
        list[str]: the names of the instances with n_machines machines
    """
    metadata = load_metadata(**kwargs)
    names = []
    for instance in metadata:
        if instance["n_machines"] == n_machines:
            names.append(instance["name"])
    return names


def train_eval_test_split_by_name(
    folder_names: list[str],
    seed: int = 0,
    test_size: float = 0.2,
    n_machines: int = 10,
) -> tuple[
    list[JobShopInstance], list[JobShopInstance], list[JobShopInstance]
]:
    """Returns the train, eval and test sets of instances. Part of the
    Difficulty Prediction task and GAN tasks.
    
    Divides the train and test instances by the name of the benchmark
    instances with the given number of machines.
    
    The train set is further divided into train and eval sets using the
    train_test_split function from scikit-learn.

    Args:
        folder_names (list[str]): the names of the folders containing the
            instances
        seed (int, optional): the seed for the train test split. Defaults to 0.
        test_size (float, optional): the proportion of instances to use for
            testing. Defaults to 0.2.
        n_machines (int, optional): the number of machines of each instance.

    Returns:
        tuple[
            list[JobShopInstance], list[JobShopInstance], list[JobShopInstance]
            ]:
            the train, eval and test sets.
    """
    instances = load_pickle_instances_from_folders(folder_names)
    instance_names = get_names_with_n_machines(n_machines)
    train, test = train_test_split_by_name(instances, instance_names)

    # Divide train into train and eval
    train, evaluation = train_test_split(
        train, test_size=test_size, random_state=seed
    )

    return train, evaluation, test