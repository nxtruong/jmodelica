package org.jmodelica.util;

/**
 * An empty <code>FormattingItem</code> used when there is no formatting.
 */
public class EmptyFormattingItem extends DefaultFormattingItem {

	/**
	 * Creates an <code>EmptyFormattingItem</code> to use when there is no formatting.
	 */
	public EmptyFormattingItem() {
		super(Type.EMPTY, null);
	}

	@Override
	public FormattingItem mergeItems(Adjacency where, FormattingItem otherItem) {
		if (!(otherItem instanceof EmptyFormattingItem)) {
			return otherItem;
		}

		return this;
	}

	@Override
	public String toString() {
		return "";
	}

}
