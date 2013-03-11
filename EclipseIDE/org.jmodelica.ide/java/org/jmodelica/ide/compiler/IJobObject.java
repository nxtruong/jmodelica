package org.jmodelica.ide.compiler;

public interface IJobObject {
	public static final int REMOVE_NODE = 1;
	public static final int ADD_NODE = 2;
	public static final int RENAME_NODE = 3;
	public static final int UPDATE = 4;

	public static final int PRIORITY_HIGH = 2;
	public static final int PRIORITY_MEDIUM = 1;
	public static final int PRIORITY_LOW = 0;

	public abstract void doJob();

	public abstract int getPriority();
}
